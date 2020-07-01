import pytest
from subprocess import call, check_output
from difflib import context_diff
import configparser, os, sys

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
    if cfg.getboolean("project", "multiplebooks"):
        bks = cfg.get("project", "booklist").split()
        filename = "{}{}_{}{}".format(cfgname, bks[0], (bks[1] if len(bks) > 1 else bks[0]), project)
    else:
        bks = cfg.get("project", "book")
        filename = "{}{}{}".format(cfgname, bks, project)
    stddir = os.path.join(projectsdir, '..', 'standards', project)
    return (stddir, filename, testsdir, ptxcmd)

def test_pdf(projectsdir, project, config):
    (stddir, filename, testsdir, ptxcmd) = make_paths(projectsdir, project, config, xdv=False)
    assert call(ptxcmd) == 0

def disabled_test_xdv(projectsdir, project, config):
    (stddir, filename, testsdir, ptxcmd) = make_paths(projectsdir, project, config, xdv=True)
    xdvcmd = [os.path.join(testsdir, "..", "python", "scripts", "xdvitype"),
                "-d"]
    if sys.platform == "win32":
        xdvcmd.insert(0, "python")

    assert call(ptxcmd) == 0
    fromfile = os.path.join(projectsdir, project, "PrintDraft", "ptxprint-"+filename+".xdv")
    tofile = os.path.join(stddir, filename+".xdv")
    resdat = check_output(xdvcmd + [fromfile]).decode("utf-8")
    stddat = check_output(xdvcmd + [tofile]).decode("utf-8")
    diff = "\n".join(context_diff(stddat.split("\n"), resdat.split("\n"), fromfile=fromfile, tofile=tofile))
    assert diff == ""

