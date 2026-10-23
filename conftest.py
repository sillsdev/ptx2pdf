
# Command line options must be registered from a conftest pytest loads at startup,
# i.e. this root one, so that they work whether pytest is run from here or test/.

def pytest_addoption(parser):
    parser.addoption("--dir", help="Project root directory to test")
    parser.addoption("-U","--update", action="store_true", default=False)
    parser.addoption("--logging")
    parser.addoption("-S", "--slow", action="store_true", default=False,
                     help="Also run slow tests: polyglot fills and configs with a standard PDF over 1MB")
