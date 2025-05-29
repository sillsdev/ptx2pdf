
import pytest, os, time

@pytest.fixture(scope="session")
def updatedata(pytestconfig):
    return pytestconfig.option.update

@pytest.fixture(scope="session")
def maxSize(pytestconfig):
    return pytestconfig.option.maxsize

@pytest.fixture(scope="session")
def logging(pytestconfig):
    return pytestconfig.option.logging

@pytest.fixture(scope="session")
def starttime(pytestconfig):
    return time.time()

def pytest_addoption(parser):
    parser.addoption("--dir", help="Project root directory to test")
    parser.addoption("-U","--update", action="store_true", default=False)
    parser.addoption("-S","--maxsize", type=float, default=10, help="Auto pass tests with > xMB regression pdf")
    parser.addoption("--logging")

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
    jobs = [j[:2] for j in sorted(jobs, key=lambda x:(-x[2], x[0], x[1]))]
    metafunc.parametrize("projectsdir", [basedir], scope="module")
    if len(jobs):
        metafunc.parametrize(("project", "config"), jobs, scope="module")
