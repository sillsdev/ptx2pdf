
import sys, subprocess, os
import xml.etree.ElementTree as et

# Thank you to rho https://stackoverflow.com/questions/10514094/gobject-and-subprocess-popen-to-communicate-in-a-gtk-gui
from gi.repository import GObject, Gtk, Pango

class StreamTextBuffer(Gtk.TextBuffer):
    def __init__(self):
        super(StreamTextBuffer, self).__init__()
        self.IO_WATCH_ID = []
        self.proc = None
        self.create_tag("bold", weight=Pango.Weight.BOLD)
        self.create_mark("currend", self.get_iter_at_offset(0), True)

    def bind_subprocess(self, proc):
        if len(self.IO_WATCH_ID):
            for id_ in self.IO_WATCH_ID:
                GObject.source_remove(id_)
            if self.proc.returncode is None:
                self.proc.terminate()
            self.proc = None
        self.IO_WATCH_ID = []
        if proc is not None:
            for p in (proc.stdout, proc.stderr):
                unblock_fd(p)
                self.IO_WATCH_ID.append(GObject.io_add_watch(
                        channel = p, priority_ = GObject.IO_IN,
                        condition = self.buffer_update))
            self.proc = proc
        return self.IO_WATCH_ID

    def buffer_update(self, stream, condition):
        self.insert_at_cursor(stream.read())
        return True

    def add_heading(self, txt):
        self.insert_at_cursor("\n")
        self.move_mark_by_name("currend", self.get_iter_at_offset(-1))
        self.insert_at_cursor(txt + "\n")
        end = self.get_iter_at_offset(-1)
        self.apply_tag_by_name("bold", self.get_iter_at_mark(self.get_mark("currend")), end)


if sys.platform == "linux":
    import os
    import fcntl

    def unblock_fd(stream):
        fd = stream.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def fclist(family, pattern):
        a = ["fc-list", '"{0}":style="{1}"'.format(family, pattern), 'file']
        # print(a)
        return subprocess.check_output(" ".join(a), shell=1).decode("utf-8")

    def checkoutput(*a, **kw):
        res = subprocess.check_output(*a, **kw).decode("utf-8")
        return res

    def call(*a, **kw):
        if kw.get('logbuffer', None) is not None:
            b = kw['logbuffer']
            del kw['logbuffer']
            b.add_heading("Execute: " + " ".join(a[0]))
            p = subprocess.Popen(*a, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.DEVNULL,
                                 universal_newlines = True, encoding="utf-8", errors="backslashreplace", bufsize=1, **kw)
            b.bind_subprocess(p)
            return p
        else:
            del kw['logbuffer']
            res = subprocess.call(*a, **kw)
            return res

    def openkey(path):
        basepath = os.path.expanduser("~/.config/paratext/registry/LocalMachine/software")
        valuepath = os.path.join(basepath, path.lower(), "values.xml")
        doc = et.parse(valuepath)
        return doc

    def queryvalue(base, value):
        res = base.getroot().find('.//value[@name="{}"]'.format(value))
        if res is None:
            return ""
        else:
            return res.text

elif sys.platform == "win32":
    import winreg
    import msvcrt

    from ctypes import windll, byref, wintypes, WinError, POINTER
    from ctypes.wintypes import HANDLE, DWORD, BOOL

    LPDWORD = POINTER(DWORD)

    SetNamedPipeHandleState = windll.kernel32.SetNamedPipeHandleState
    SetNamedPipeHandleState.argtypes = [HANDLE, LPDWORD, LPDWORD, LPDWORD]
    SetNamedPipeHandleState.restype = BOOL

    def unblock_fd(stream):
        PIPE_NOWAIT = wintypes.DWORD(0x00000001)
        h = msvcrt.get_osfhandle(stream.fileno())
        res = windll.kernel32.SetNamedPipeHandleState(h, byref(PIPE_NOWAIT), None, None)
        if res == 0:
            print(WinError())
            return False
        return True

    def openkey(path):
        return winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\\" + path.replace("/", "\\"))

    def queryvalue(base, value):
        return winreg.QueryValueEx(base, value)[0]

    def fclist(family, pattern):
        a = [os.path.join(pt_bindir, "xetex", "bin", "fc-list.exe").replace("\\", "/"),
                '"'+family+'"', '":style='+pattern+'"', 'file']
        return subprocess.check_output(a).decode("utf-8")

    def checkoutput(*a, **kw):
        if 'shell' in kw:
            del kw['shell']
        path = os.path.join(pt_bindir, "xetex", "bin", a[0][0]+".exe").replace("\\", "/")
        newa = [[path] + list(a[0])[1:]] + [x.replace('"', '') for x in a[1:]]
        # print(newa)
        res = subprocess.check_output(*newa, **kw).decode("utf-8")
        return res

    def call(*a, **kw):
        path = os.path.join(pt_bindir, "xetex", "bin", a[0][0]+".exe").replace("/", "\\")
        newa = [[path] + a[0][1:]] + list(a)[1:]
        del kw['logbuffer'] # Temporary hack as a work-around. Remove later.
        if 'logbuffer' in kw:
            b = kw['logbuffer']
            del kw['logbuffer']
            b.add_heading("Execute: " + " ".join(a[0]))
            p = subprocess.Popen(*newa, stdout = subprocess.PIPE, stderr = subprocess.PIPE,
                                 universal_newlines = True, encoding="utf-8", errors="backslashreplace", **kw)
            b.bind_subprocess(p)
            return p
        else:
            res = subprocess.call(*newa, **kw)
            return res

# print("before ptob")
ptob = openkey("Paratext/8")
pt_settings = "."
# print("ptob {} before ptv".format(ptob))
try:
    ptv = queryvalue(ptob, "ParatextVersion")
    # print("after ptv")
except FileNotFoundError:
    # print("Within Except") 
    for v in ('9', '8'):
        path = "C:\\My Paratext {} Projects".format(v)
        if os.path.exists(path):
            pt_settings = path
            pt_bindir = "C:\\Program Files (x86)\\Paratext {}".format(v)
            break
else:
    if ptv:
        version = ptv[:ptv.find(".")]
        pt_bindir = queryvalue(ptob, 'Program_Files_Directory_Ptw'+version)
    pt_settings = queryvalue(ptob, 'Settings_Directory')
if ptv:
    print("Paratext Projects Folder: ",pt_settings,"\nParatext Program Folder:  ",pt_bindir)
