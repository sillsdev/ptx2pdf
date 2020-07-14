import pytest
import unittest
from subprocess import call, check_output
from difflib import context_diff
import configparser, os, sys, shutil
from ptxprint.ptsettings import ParatextSettings
from collections import namedtuple

def make_paths(projectsdir, project, config, xdv=False):
    testsdir = os.path.dirname(__file__)
    ptxcmd = [os.path.join(testsdir, "..", "python", "scripts", "ptxprint"),
                "--nofontcache",
                "-p", projectsdir, "-f", os.path.join(testsdir, "fonts")]
    if xdv:
        ptxcmd += ["-T"]
    if config is not None:
        ptxcmd += ['-c', config]
    ptxcmd += ["-P", project]
    if sys.platform == "win32":
        ptxcmd.insert(0, "python")
    cfg = configparser.ConfigParser()
    if config is not None:
        configpath = os.path.join(projectsdir, project, "shared", "ptxprint", config, "ptxprint.cfg")
        cfgname = config + "-"
    else:
        configpath = os.path.join(projectsdir, project, "shared", "ptxprint", "ptxprint.cfg")
        cfgname = ""
    cfg.read(configpath, encoding="utf-8")
    ptsettings = ParatextSettings(projectsdir, project)
    if cfg.getboolean("project", "multiplebooks"):
        bks = [x for x in cfg.get("project", "booklist").split() \
            if os.path.exists(os.path.join(projectsdir, project, ptsettings.getBookFilename(x)))]
    else:
        bks = [cfg.get("project", "book")]
    if len(bks) > 1:
        filename = "{}{}_{}{}".format(cfgname, bks[0], bks[-1], project)
    else:
        filename = "{}{}{}".format(cfgname, bks[0], project)
    stddir = os.path.join(projectsdir, '..', 'standards', project)
    return (stddir, filename, testsdir, ptxcmd)

XdvInfo = namedtuple("XdvInfo", ["projectsdir", "project", "config", "stddir", "filename", "filebasepath", "testsdir"])

@pytest.fixture(scope="class")
def xdv(request, projectsdir, project, config):
    (stddir, filename, testsdir, ptxcmd) = make_paths(projectsdir, project, config, xdv=True)
    assert call(ptxcmd) == 0
    filebasepath = os.path.join(projectsdir, project, "PrintDraft", "ptxprint-"+filename)
    yield XdvInfo(projectsdir, project, config, stddir, filename, filebasepath, testsdir)

@pytest.mark.usefixtures("xdv")
class TestXetex:
    def test_pdf(self, xdv):
        xdvcmd = "xdvipdfmx -q -E -o " + xdv.filebasepath+".pdf"
        assert call(xdvcmd, shell=True)

    def test_xdv(self, xdv):
        xdvcmd = [os.path.join(xdv.testsdir, "..", "python", "scripts", "xdvitype"), "-d"]
        if sys.platform == "win32":
            xdvcmd.insert(0, "python")

        fromfile = xdv.filebasepath+".xdv"
        tofile = os.path.join(xdv.stddir, xdv.filename+".xdv")
        if not os.path.exists(tofile) and os.path.exists(fromfile):
            shutil.copy(fromfile, tofile)
            pytest.xfail("No regression xdv. Copying...")
        resdat = check_output(xdvcmd + [fromfile]).decode("utf-8")
        stddat = check_output(xdvcmd + [tofile]).decode("utf-8")
        diff = "\n".join(context_diff(stddat.split("\n"), resdat.split("\n"), fromfile=fromfile, tofile=tofile))
        if diff != "":
            pytest.xfail("xdvs are inconsistent")
