""" Replay each GUI test kept in a test project (projects/<project>/shared/tests/<config>/*.zip,
    made with mkguitest.py or recorded with `ptxprint -C test.zip --lean`) and check that it
    changes the same files in the same way. The tests run on copies of the projects, under a
    broadway display. """

import os, sys, glob, shutil, subprocess
import pytest

testsdir = os.path.dirname(os.path.abspath(__file__))
guitests = sorted(glob.glob(os.path.join(testsdir, "projects", "*", "shared", "tests", "*", "*.zip")))

def _testid(t):
    parts = t.split(os.sep)
    return "{}/{}/{}".format(parts[-5], parts[-2], os.path.splitext(parts[-1])[0])

def _cantRun():
    if shutil.which("broadwayd") is None:
        return "broadwayd is not installed"
    try:
        import gi
        gi.require_version("Gtk", "3.0")
    except (ImportError, ValueError) as e:
        return f"GTK is not available: {e}"
    return None

@pytest.mark.skipif(_cantRun() is not None, reason=str(_cantRun()))
@pytest.mark.parametrize("testfile", guitests, ids=[_testid(t) for t in guitests])
def test_gui(testfile, tmp_path):
    env = dict(os.environ)
    for v in ("DISPLAY", "WAYLAND_DISPLAY"):    # never use a real screen
        env.pop(v, None)
    for v, d in (("XDG_RUNTIME_DIR", "run"), ("XDG_CONFIG_HOME", "config"), ("XDG_DATA_HOME", "data")):
        env[v] = str(tmp_path / d)
        os.makedirs(env[v], mode=0o700)
    args = [sys.executable, os.path.join(testsdir, "..", "python", "scripts", "ptxprint"),
            "-q", "-N", "-t", testfile]
    res = subprocess.run(args, env=env, capture_output=True, text=True, encoding="utf-8",
                         errors="replace", timeout=300)
    out = "\n".join(l for l in res.stdout.splitlines() if l.strip())
    assert res.returncode == 0 and "Test result: PASS" in out, out + "\n" + res.stderr[-3000:]
