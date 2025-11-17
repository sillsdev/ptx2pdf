import pytest
import unittest
import subprocess
import re
from difflib import context_diff
import configparser, os, sys, shutil
from ptxprint.ptsettings import ParatextSettings
from collections import namedtuple
# from filelock import FileLock

def myremove(x):
    print(f"Removing {x}")

def w2u(path, endwithslash=True):
    """Windows to Unix filepath converter"""
    if path == "":
        return ""
    else:
        path = path.replace("\\", "/")
        return (path + ("/" if endwithslash else "")).replace("//", "/")

def quote(path):
    if " " in path:
        return '"' + path.strip('"') + '"'
    else:
        return path
    
if False and sys.platform == "win32":
    import winreg
    def queryvalue(base, value):
        return winreg.QueryValueEx(base, value)[0]
    
    def openkey(path):
        return winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\\" + path.replace("/", "\\"))

    ptob = openkey("Paratext/8")
    pt_settings = "."
    try:
        ptv = queryvalue(ptob, "ParatextVersion")
    except FileNotFoundError:
        for v in ('9', '8'):
            path = "C:\\My Paratext {} Projects".format(v)
            if os.path.exists(path):
                pt_settings = path
                pt_bindir = "C:\\Program Files (x86)\\Paratext {}".format(v)
                break
    else:
        if ptv:
            version = ptv[:ptv.find(".")]
            pt_bindir = queryvalue(ptob, 'Program_Files_Directory_Ptw'+version)
        pt_settings = queryvalue(ptob, 'Settings_Directory')
    
    pt_bindir = pt_bindir + ("\\" if pt_bindir[-1] != "\\" else "") + "xetex\\bin\\windows\\"
    
else:
    pt_bindir = ""

def call(*a, **kw):
    print("Calling", a, kw)
    return subprocess.call(*a, **kw)

def check_output(*a, **kw):
    print("Capturing", a, kw)
    return subprocess.check_output(*a, **kw)

def make_paths(projectsdir, project, config, logging):
    testsdir = os.path.dirname(__file__)
    ptxcmd = [os.path.join(testsdir, "..", "python", "scripts", "ptxprint"), "-p", projectsdir,
                "--testsuite", "--nofontcache", "-l", "info", f"--logfile=ptxprint_{project}_{config}.log",
                "-f", os.path.join(testsdir, "fonts")]
    if config is not None:
        ptxcmd += ['-c', config]
    if logging is not None:
        ptxcmd += ['-l', logging]
    ptxcmd += [project]
    if sys.platform == "win32":
        ptxcmd.insert(0, "python")
    cfg = configparser.ConfigParser()
    if config is not None:
        configpath = os.path.join(projectsdir, project, "shared", "ptxprint", config, "ptxprint.cfg")
        cfgname = "_" + config
    else:
        configpath = os.path.join(projectsdir, project, "shared", "ptxprint", "ptxprint.cfg")
        cfgname = ""
    cfg.read(configpath, encoding="utf-8")
    ptsettings = ParatextSettings(os.path.join(projectsdir, project))
    try:
        ismult = cfg.get("project", "bookscope") == "multiple"
    except configparser.NoOptionError:
        ismult = cfg.getboolean("project", "multiplebooks")
    if ismult:
        bks = []
        bks = [x for x in cfg.get("project", "booklist").split() \
            if os.path.exists(os.path.join(projectsdir, project, ptsettings.getBookFilename(x)))]
    else:
        prjmode = cfg.get("project", "bookscope")
        if prjmode == "module":
            mod = os.path.basename(cfg.get("project", "modulefile"))
            bks = [os.path.splitext(mod)[0]]
        else:
            bks = [cfg.get("project", "book")]
    if len(bks) > 1:
        filename = "{}{}_{}-{}_ptxp".format(project, cfgname, bks[0], bks[-1])
    else:
        filename = "{}{}_{}_ptxp".format(project, cfgname, bks[0])
    stddir = os.path.join(projectsdir, '..', 'standards', project)
    return (stddir, filename, testsdir, ptxcmd)

PdfInfo = namedtuple("PdfInfo", ["project", "config", "pdfpath", "stdpath", "diffpath",
                                 "arcpath", "ptxcmd", "result", "resulta"])

@pytest.fixture(scope="class")
def pdf(request, projectsdir, project, config, starttime, logging, maxSize):
    (stddir, filename, testsdir, ptxcmd) = make_paths(projectsdir, project, config, logging)
    pdftpath = os.path.join(projectsdir, project, "local", "ptxprint")
    cfglocal = os.path.join(pdftpath, config)
    os.makedirs(os.path.join(pdftpath, config), exist_ok=True)
    pdffile = "{}.pdf".format(filename)
    pdfpath = os.path.join(pdftpath, pdffile)
    stdpath = os.path.join(stddir, pdffile)
    if maxSize > 0 and os.path.exists(stdpath):
        if os.path.getsize(stdpath) > maxSize * 1000000:
            request.cls.pdf = None
            return
    diffpath = pdfpath.replace(".pdf", "_diff.pdf")
    try:
        os.remove(diffpath)
    except FileNotFoundError:
        pass
    for a in (".parlocs", ".delayed", ".notepages", ".picpages"):
        fpath = os.path.join(cfglocal, filename + a)
        print(f"removing {fpath}")
        try:
            os.remove(fpath)
        except FileNotFoundError:
            pass
    pdfptxcmd = ptxcmd[:-1] + ["-P", "-F", stdpath, "--diffpages=50"] + ptxcmd[-1:]
    res = call(pdfptxcmd)
    assert res != 1
    arcpath = os.path.join(pdftpath, config, "ptxprintArchive.zip")
    aptxcmd = ptxcmd[:-1] + ["-A", "createArchive"] + ptxcmd[-1:]
    try:
        os.remove(arcpath)
    except FileNotFoundError:
        pass
    resa = call(aptxcmd)
    assert resa == 0
    request.cls.pdf = PdfInfo(project, config, pdfpath, stdpath, diffpath, arcpath, ptxcmd, res, resa)

@pytest.mark.usefixtures("pdf")
class TestXetex:
    def test_pdf(self, updatedata):
        if self.pdf is None:
            return
        msg = None
        if self.pdf.result == 2:
            msg = "missing base pdf"
        elif os.path.exists(self.pdf.diffpath):
            msg = "pdfs are inconsistent"
        #else:
        #    return
        if updatedata:
            shutil.copy(self.pdf.pdfpath, self.pdf.stdpath)

        outfname = os.path.join(os.path.dirname(self.pdf.arcpath), "testArchive_diff.pdf")
        print(f"{outfname=}")
        try:
            os.remove(outfname)
        except FileNotFoundError:
            pass
        ptxcmd = self.pdf.ptxcmd
        # ptxprint -p basedir ... <project>
        ptxcmd = ptxcmd[:2] + ["tmp"] + ptxcmd[3:-1] + ["-Z", self.pdf.arcpath, "-F", self.pdf.pdfpath,
                                "--diffpages=50", "--diffoutfile="+outfname, "-P"] + ptxcmd[-1:]
        print(f"exists({os.path.dirname(self.pdf.arcpath)}) = {os.path.exists(os.path.dirname(self.pdf.arcpath))}")
        res = call(ptxcmd)
        assert res != 1
        if os.path.exists(outfname):
            msg = "archive pdf is different"
        if msg is not None:
            pytest.xfail(msg)

