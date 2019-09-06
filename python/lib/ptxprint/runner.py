
import sys, subprocess
import xml.etree.ElementTree as et

if sys.platform == "linux":
    import os

    def call(*a, **kw):
        res = subprocess.check_output(*a, **kw).decode("utf-8")
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

    def openkey(path):
        return winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\\" + path.replace("/", r"\\"))

    def queryvalue(base, value):
        return winreg.QueryValue(base, value)

    def call(*a, **kw):
        path = os.path.join(pt_bindir, "xetex", "bin", a[0][0]+".exe")
        newa = [path] + a[1:]
        res = subprocess.check_output(*a, **kw).decode("utf-8")
        return res

ptob = openkey("Paratext/8")
ptv = queryvalue(ptob, "ParatextVersion")
if ptv:
    version = ptv[:ptv.find(".")]
    pt_bindir = queryvalue(ptob, 'Program_Files_Directory_Ptw'+version)
pt_settings = queryvalue(ptob, 'Settings_Directory')
