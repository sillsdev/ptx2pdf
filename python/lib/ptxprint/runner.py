
import sys, subprocess, os
import xml.etree.ElementTree as et
from ptxprint.utils import pt_bindir

# Thank you to rho https://stackoverflow.com/questions/10514094/gobject-and-subprocess-popen-to-communicate-in-a-gtk-gui
from gi.repository import GObject, Gtk, Pango

# StreamTextBuffer removed post v1.5.6

if sys.platform == "linux":

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
        a = [os.path.join(pt_bindir(), "xetex", "bin", "fc-list.exe").replace("\\", "/"),
                '"'+family+'"', '":style='+pattern+'"', 'file']
        return subprocess.check_output(a, creationflags=CREATE_NO_WINDOW).decode("utf-8", errors="ignore")

    def checkoutput(*a, **kw):
        if 'shell' in kw:
            del kw['shell']
        if 'path' in kw:
            if kw['path'] == 'xetex':
                path = os.path.join(pt_bindir(), "xetex", "bin", a[0][0]+".exe").replace("\\", "/")
                a = [[path] + list(a[0])[1:]] + [x.replace('"', '') for x in a[1:]]
            del kw['path']
        else:
            a = [[x.replace("/", "\\") for x in a[0]]] + [x.replace('"', '') for x in a[1:]]
        res = subprocess.check_output(*a, creationflags=CREATE_NO_WINDOW, **kw).decode("utf-8", errors="ignore")
        return res

    def call(*a, **kw):
        path = os.path.join(pt_bindir(), "xetex", "bin", a[0][0]+".exe").replace("/", "\\")
        newa = [[path] + a[0][1:]] + list(a)[1:]
        if 'logbuffer' in kw:
            del kw['logbuffer'] # Temporary hack as a work-around. Remove later.
        res = subprocess.call(*newa, creationflags=CREATE_NO_WINDOW, **kw)
        return res

