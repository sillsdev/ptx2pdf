
import os
from dataclasses import dataclass
from ptxprint.ptsettings import ParatextSettings
import logging

logger = logging.getLogger(__name__)

@dataclass
class ProjectDir:
    prjid: str
    guid: str
    path: str

@dataclass
class ConfigDir:
    cfgid: str
    path: str

NullConfigDir = ConfigDir("", "")

class ProjectList:
    def __init__(self):
        self.treedirs = []
        self.projects = {}      # indexed by guid
        self.ptxdir = None

    def __len__(self):
        return len(self.projects)

    def addTreedir(self, path, isptx=False):
        path = os.path.abspath(path)
        if path in self.treedirs:
            return False
        try:
            sdir = os.listdir(path)
        except FileNotFoundError:
            return False
        self.treedirs.append(path)

        for d in sdir:
            p = os.path.join(path, d)
            if not os.path.isdir(p):
                continue
            if "." in d:
                name = d[:d.index(".")]
            else:
                name = d
            addme = False
            guid = None
            for a in ('Settings.xml', 'ptxSettings.xml'):
                if os.path.exists(os.path.join(p, a)):
                    with open(os.path.join(p, a), encoding="utf-8") as inf:
                        addme = True
                        guid = None
                        for l in inf.readlines():
                            if '<TranslationInfo>' in l:
                                if 'ConsultantNotes:'  in l or 'StudyBibleAdditions:' in l:
                                    addme = False
                            if '<Guid>' in l:
                                guid = l[l.find("<Guid>")+6:l.rfind("<")]
            if guid is None:
                if any(x.lower().endswith("sfm") for x in os.listdir(p)):
                    addme = True
                if addme:
                    pt = ParatextSettings(p)
                    guid = pt['Guid']
                    if pt.saveme:
                        pt.saveAs(os.path.join(p, "ptxSettings.xml"))
            if addme:
                self.addProject(name, p, guid)
        if isptx:
            for s in ("_projectById", "_PTXprint"):
                p = os.path.join(path, s)
                if os.path.exists(p):
                    self.addTreedir(p)
            self.ptxdir = path
        return True

    def addProject(self, prjid, path, guid):
        pt = None
        if guid is None:
            pt = ParatextSettings(path)
            guid = pt['Guid']
        if guid in self.projects:
            if self.projects[guid].path != path:
                if pt is None:
                    pt = ParatextSettings(path)
                guid = pt.createGuid()
                pt.saveAs(os.path.join(path, 'ptxSettings.xml'))
            else:
                return None
        p = ProjectDir(prjid, guid, path)
        logger.debug(f"Adding project {p}")
        self.projects[guid] = p
        return p

    def getProject(self, guid):
        p = self.projects.get(guid, None)
        logger.debug(f"Seeking project {guid} found {p}")
        if p is None:
            return None
        return Project(p)

    def projectList(self):
        return sorted(self.projects.values(), key=lambda s:(s.prjid.lower(), s.path, s.guid))

    def findProject(self, prjid):
        for t in self.treedirs:
            p = os.path.join(t, prjid)
            for g, v in self.projects.items():
                if v.path == p:
                    return Project(v)
        return None

    def findFile(self, fname):
        for t in self.treedirs:
            p = os.path.join(t, fname)
            if os.path.exists(p):
                return p
        return None

    def findWriteable(self):
        for t in self.treedirs:
            if "_PTXprint" in t:
                return t
        if self.ptxdir is None:
            t = os.path.join(self.treedirs[0], "_PTXprint")
        else:
            t = os.path.join(self.ptxdir, "_PTXprint")
        os.makedirs(t, exist_ok=True)
        self.addTreedir(t)
        return t

    def addToConfig(self, config, section="projectdirs"):
        config.remove_section(section)
        config.add_section(section)
        for i, d in enumerate(self.treedirs, 1):
            config.set(section, str(i), d)


class Project:
    shareddir = "shared/ptxprint"
    localdir = "local/shared/ptxprint"
    printdir = "local/ptxprint"

    def __init__(self, prjdir):
        self.prjid = prjdir.prjid
        self.path = prjdir.path
        self.guid = prjdir.guid
        self.configs = {}
        self.findConfigs(self.path)

    def __repr__(self):
        return f"{self.prjid}[{self.guid}] {self.path}"

    def findConfigs(self, path):
        for a in (self.shareddir, self.localdir):
            cpath = os.path.join(path, a)
            if not os.path.exists(cpath) or not os.path.isdir(cpath):
                continue
            for d in os.listdir(cpath):
                p = os.path.join(cpath, d)
                if not os.path.isdir(p) or not os.path.exists(os.path.join(p, "ptxprint.cfg")):
                    continue
                if d not in self.configs:
                    self.configs[d] = ConfigDir(d, p)

    def srcPath(self, cfgid=None, makepath=False):
        if cfgid is None:
            return os.path.join(self.path, self.shareddir)
        res = self.configs.get(cfgid, NullConfigDir).path
        if makepath and res is None:
            if self.createConfigDir(cfgid):
                return self.configs.get(cfgid, NullConfigDir).path
        return res

    def printPath(self, cfgid):
        if cfgid is None:
            return os.path.join(self.path, self.printdir)
        return os.path.join(self.path, self.printdir, cfgid)

    def shareConfig(self, cfgid, toshared=True):
        cdir = self.configs.get(cfgid, None)
        if cdir is None:
            return False
        ldir = os.path.join(self.path, self.localdir, cfgid)
        sdir = os.path.join(self.path, self.shareddir, cfgid)
        isshared = sdir == cdir
        if isshared == toshared:
            return False
        ddir = sdir if toshared else ldir
        copytree(cdir, ddir, symlinks=True, dirs_exist_ok=True)
        self.configs[cfgid] = ConfigDir(cfgid, ddir)
        return True

    def createConfigDir(self, cfgid, shared=True, test=False):
        testres = False
        if cfgid not in self.configs:
            ddir = os.path.join(self.path, self.shareddir if shared else self.localdir, cfgid)
            testres = not os.path.exists(ddir)
            os.makedirs(ddir, exist_ok=True)
            self.configs[cfgid] = ConfigDir(cfgid, ddir)
        res = self.configs[cfgid].path
        return (res, testres) if test else res 


