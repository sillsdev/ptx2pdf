
import sys, subprocess, os, logging
import xml.etree.ElementTree as et
from ptxprint.utils import pt_bindir

logger = logging.getLogger(__name__)

if sys.platform == "linux" or sys.platform == "darwin":

    def fclist(family, pattern):
        a = ["fc-list", '"{0}":style="{1}"'.format(family, pattern), 'file']
        return subprocess.check_output(" ".join(a), shell=1).decode("utf-8", errors="ignore")

    def checkoutput(*a, **kw):
        if 'path' in kw:
            del kw['path']
        res = subprocess.check_output(*a, **kw).decode("utf-8", errors="ignore")
        return res

    def call(*a, **kw):
        return subprocess.call(*a, **kw)

elif sys.platform == "win32":
    CREATE_NO_WINDOW = 0x08000000

    def fclist(family, pattern):
        a = [os.path.join(pt_bindir(), "xetex", "bin", "windows", "fc-list.exe").replace("\\", "/"),
                '"'+family+'"', '":style='+pattern+'"', 'file']
        return subprocess.check_output(a, creationflags=CREATE_NO_WINDOW).decode("utf-8", errors="ignore")

    def checkoutput(*a, **kw):
        if 'shell' in kw:
            del kw['shell']
        if 'path' in kw:
            if kw['path'] == 'xetex':
                path = os.path.join(pt_bindir(), "xetex", "bin", "windows", a[0][0]+".exe").replace("\\", "/")
                a = [[path] + list(a[0])[1:]] + [x.replace('"', '') for x in a[1:]]
            del kw['path']
        else:
            a = [[x.replace("/", "\\") for x in a[0]]] + [x.replace('"', '') for x in a[1:]]
        res = subprocess.check_output(*a, creationflags=CREATE_NO_WINDOW, **kw).decode("utf-8", errors="ignore")
        return res

    def call(*a, **kw):
        path = os.path.join(pt_bindir(), "xetex", "bin", "windows", a[0][0]+".exe").replace("/", "\\")
        newa = [[path] + a[0][1:]] + list(a)[1:]
        logger.debug(f"{path=} {newa=}")
        kw['stdout'] = kw.get('stdout', subprocess.PIPE)
        kw['stderr'] = kw.get('stderr', subprocess.STDOUT)
        res = subprocess.run(*newa, creationflags=CREATE_NO_WINDOW, **kw)
        return res

