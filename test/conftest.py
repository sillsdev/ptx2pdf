
import pytest, os, time

@pytest.fixture(scope="session")
def updatedata(pytestconfig):
    return pytestconfig.option.update

@pytest.fixture(scope="session")
def logging(pytestconfig):
    return pytestconfig.option.logging

@pytest.fixture(scope="session")
def starttime(pytestconfig):
    return time.time()

# Command line options are in ../conftest.py, so they work from the repo root too.

def pytest_generate_tests(metafunc):
    jobs = []
    basedir = metafunc.config.getoption("dir")
    if basedir is None:
        basedir = os.path.join(os.path.dirname(__file__), 'projects')
    for b in os.listdir(basedir):
        bbase = os.path.join(basedir, b, "shared", "ptxprint")
        if b.startswith(".") or not os.path.exists(bbase):
            continue
        for c in os.listdir(bbase):
            if c.startswith(".") or c.startswith("_"):
                continue
            if c == "ptxprint.cfg":
                c = None
            elif not os.path.exists(os.path.join(bbase, c, "ptxprint.cfg")):
                continue
            sdir = os.path.join(basedir, '..', 'standards', b)
            size = 0
            for sfile in os.listdir(sdir):
                if sfile.startswith(f"{b}_{c}_"):
                    size = os.stat(os.path.join(sdir, sfile)).st_size
                    break
            jobs.append((b, c, size))
    # print("generating tests", basedir, jobs)
    # A config with a standard PDF over 1MB is slow
    jobs = [pytest.param(*j[:2], marks=pytest.mark.slow) if j[2] > 1000000 else j[:2]
                for j in sorted(jobs, key=lambda x:(-x[2], x[0], x[1]))]
    metafunc.parametrize("projectsdir", [basedir], scope="module")
    if len(jobs):
        metafunc.parametrize(("project", "config"), jobs, scope="module")

def pytest_configure(config):
    config.addinivalue_line("markers", "slow: slow test, only run with --slow")

def pytest_collection_modifyitems(config, items):
    if config.getoption("slow", default=False):
        return
    skipslow = pytest.mark.skip(reason="slow: use --slow to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skipslow)
