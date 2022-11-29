
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

def pytest_addoption(parser):
    parser.addoption("--dir", help="Project root directory to test")
    parser.addoption("-U","--update", action="store_true", default=False)
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
                jobs.append((b, None))
            elif os.path.exists(os.path.join(bbase, c, "ptxprint.cfg")):
                jobs.append((b, c))
    # print("generating tests", basedir, jobs)
    metafunc.parametrize("projectsdir", [basedir], scope="module")
    if len(jobs):
        metafunc.parametrize(("project", "config"), jobs, scope="module")
