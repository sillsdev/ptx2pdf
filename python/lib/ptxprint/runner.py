
import sys, subprocess, os, logging, platform
import xml.etree.ElementTree as et
from ptxprint.utils import pt_bindir

logger = logging.getLogger(__name__)

architectures = {k:k for k in ("arm64", "x86_64")}
bindir = sys.platform + "_" + architectures.get(platform.machine(), "x86_64")

if sys.platform == "linux":
    import resource

    def fclist(family, pattern):
        a = ["fc-list", '"{0}":style="{1}"'.format(family, pattern), 'file']
        return subprocess.check_output(" ".join(a), shell=1).decode("utf-8", errors="ignore")

    def checkoutput(*a, **kw):
        if 'path' in kw:
            del kw['path']
        res = subprocess.check_output(*a, **kw).decode("utf-8", errors="ignore")
        return res

    def call(*a, **kw):
        return subprocess.Popen(*a, **kw)

    def popen(*a, **kw):
        return subprocess.Popen(*a, **kw)

    def child_cpu_time(runner):
        usage = resource.getrusage(resource.RUSAGE_CHILDREN)
        return (usage.ru_utime + usage.ru_stime)

elif sys.platform == "darwin":
    import resource

    def fclist(family, pattern):
        # os.putenv('TEXMFCNF', os.path.join(pt_bindir(), "xetex", "texmf_dist", "web2c"))
        a = [os.path.join(pt_bindir(), "xetex", "bin", bindir, "fc-list").replace("\\", "/"),
                '"'+family+'"', '":style='+pattern+'"', 'file']
        return subprocess.check_output(a).decode("utf-8", errors="ignore")

    def checkoutput(*a, **kw):
        if 'shell' in kw:
            del kw['shell']
        if 'path' in kw:
            if kw['path'] == 'xetex':
                # os.putenv('TEXMFCNF', os.path.join(pt_bindir(), "xetex", "texmf_dist", "web2c"))
                path = os.path.join(pt_bindir(), "xetex", "bin", bindir, a[0][0]).replace("\\", "/")
                a = [[path] + list(a[0])[1:]] + [x.replace('"', '') for x in a[1:]]
            del kw['path']
        else:
            a = [[x.replace("/", "\\") for x in a[0]]] + [x.replace('"', '') for x in a[1:]]
        res = subprocess.check_output(*a, **kw).decode("utf-8", errors="ignore")
        return res

    def call(*a, **kw):
        # os.putenv('TEXMFCNF', os.path.join(pt_bindir(), "xetex", "texmf_dist", "web2c"))
        path = os.path.join(pt_bindir(), "xetex", "bin", bindir, a[0][0]).replace("\\", "/")
        newa = [[path] + a[0][1:]] + list(a)[1:]
        logger.debug(f"{path=} {newa=}")
        kw['stdout'] = kw.get('stdout', subprocess.PIPE)
        kw['stderr'] = kw.get('stderr', subprocess.STDOUT)
        res = subprocess.Popen(*newa, **kw)
        return res

    def popen(*a, **kw):
        return subprocess.Popen(*a, **kw)

    def child_cpu_time(runner):
        usage = resource.getrusage(resource.RESOURCE_CHILDREN)
        return (usage.ru_utime + usage.ru_stime)

elif sys.platform == "win32":
    import ctypes
    from ctypes import wintypes

    CREATE_NO_WINDOW = 0x08000000

    def fclist(family, pattern):
        # os.putenv('TEXMFCNF', os.path.join(pt_bindir(), "xetex", "texmf_dist", "web2c"))
        a = [os.path.join(pt_bindir(), "xetex", "bin", bindir, "fc-list.exe").replace("\\", "/"),
                '"'+family+'"', '":style='+pattern+'"', 'file']
        return subprocess.check_output(a, creationflags=CREATE_NO_WINDOW).decode("utf-8", errors="ignore")

    def checkoutput(*a, **kw):
        if 'shell' in kw:
            del kw['shell']
        if 'path' in kw:
            if kw['path'] == 'xetex':
                # os.putenv('TEXMFCNF', os.path.join(pt_bindir(), "xetex", "texmf_dist", "web2c"))
                path = os.path.join(pt_bindir(), "xetex", "bin", bindir, a[0][0]+".exe").replace("/", "\\")
                a = [[path] + list(a[0])[1:]] + [x.replace('"', '') for x in a[1:]]
            del kw['path']
        else:
            a = [[x.replace("/", "\\") for x in a[0]]] + [x.replace('"', '') for x in a[1:]]
        res = subprocess.check_output(*a, creationflags=CREATE_NO_WINDOW, **kw).decode("utf-8", errors="ignore")
        return res

    def call(*a, **kw):
        # os.putenv('TEXMFCNF', os.path.join(pt_bindir(), "xetex", "texmf_dist", "web2c"))
        path = os.path.join(pt_bindir(), "xetex", "bin", bindir, a[0][0]+".exe").replace("/", "\\")
        newa = [[path] + a[0][1:]] + list(a)[1:]
        logger.debug(f"{path=} {newa=}, PATH={os.getenv('PATH')}")
        kw['stdout'] = kw.get('stdout', subprocess.PIPE)
        kw['stderr'] = kw.get('stderr', subprocess.STDOUT)
        res = subprocess.Popen(*newa, creationflags=CREATE_NO_WINDOW, **kw)
        return res

    def popen(*a, **kw):
        return subprocess.Popen(*a, **kw)

    def _filetime(ft):
        return (ft.dwHighDateTime << 32 | ft.dwLowDateTime) / 10_000_000

    def child_cpu_time(runner):
        if runner is None:
            return 0.
        creation_t = wintypes.FILETIME()
        exit_t = wintypes.FILETIME()
        kernel_t = wintypes.FILETIME()
        user_t = wintypes.FILETIME()
        if ctypes.windll.kernel32.GetProcessTimes(runner._handle,
                ctypes.byref(creation_t), ctypes.byref(exit_t), ctypes.byref(kernel_t),
                ctypes.byref(user_t)):
            return _filetime(user_t) + _filetime(kernel_t)
        return 0.

