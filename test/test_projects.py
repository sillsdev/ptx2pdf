import pytest
from subprocess import call, check_output
from difflib import context_diff
import configparser, os, sys

def test_projects(projectsdir, project, config):
    testsdir = os.path.dirname(__file__)
    ptxcmd = [os.path.join(testsdir, "..", "python", "scripts", "ptxprint"),
                "--nofontcache",
                "-p", projectsdir, "-f", os.path.join(testsdir, "fonts"), "-T"]
    if config is not None:
        ptxcmd += ['-c', config]
    ptxcmd += ["-P", project]
    xdvcmd = [os.path.join(testsdir, "..", "python", "scripts", "xdvitype"),
                "-d"]
    if sys.platform == "win32":
        ptxcmd.insert(0, "python")
        xdvcmd.insert(0, "python")
    cfg = configparser.ConfigParser()
    if config is not None:
        configpath = os.path.join(projectsdir, project, "shared", "ptxprint", config, "ptxprint.cfg")
    else:
        configpath = os.path.join(projectsdir, project, "shared", "ptxprint", "ptxprint.cfg")
    cfg.read(configpath)
    if cfg.getboolean("project", "multiplebooks"):
        bks = cfg.get("project", "booklist").split()
        filename = "{}_{}{}".format(bks[0], bks[1], project)
    else:
        bks = cfg.get("project", "book")
        filename = "{}{}".format(bks, project)
    stddir = os.path.join(projectsdir, '..', 'standards', project)
    
    assert call(ptxcmd) == 0
    fromfile = os.path.join(projectsdir, project, "PrintDraft", "ptxprint-"+filename+".xdv")
    tofile = os.path.join(stddir, filename+".xdv")
    resdat = check_output(xdvcmd + [fromfile]).decode("utf-8")
    stddat = check_output(xdvcmd + [tofile]).decode("utf-8")
    diff = "\n".join(context_diff(stddat.split("\n"), resdat.split("\n"), fromfile=fromfile, tofile=tofile))
    assert diff == ""

