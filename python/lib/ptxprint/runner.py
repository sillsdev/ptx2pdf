
import sys, subprocess, os
import xml.etree.ElementTree as et

if sys.platform == "linux":
    import os

    def checkoutput(*a, **kw):
        res = subprocess.check_output(*a, **kw).decode("utf-8")
        return res

    def call(*a, **kw):
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

    def openkey(path):
        return winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\\" + path.replace("/", "\\"))

    def queryvalue(base, value):
        return winreg.QueryValueEx(base, value)[0]

    def checkoutput(*a, **kw):
        path = os.path.join(pt_bindir, "xetex", "bin", a[0][0]+".exe").replace("/", "\\")
        newa = [path] + list(a)[1:]
        res = subprocess.check_output(*newa, **kw).decode("utf-8")
        return res

    def call(*a, **kw):
        path = os.path.join(pt_bindir, "xetex", "bin", a[0][0]+".exe").replace("/", "\\")
        newa = [[path] + a[0][1:]] + list(a)[1:]
        res = subprocess.call(*newa, **kw)
        return res

ptob = openkey("Paratext/8")
ptv = queryvalue(ptob, "ParatextVersion")
if ptv:
    version = ptv[:ptv.find(".")]
    pt_bindir = queryvalue(ptob, 'Program_Files_Directory_Ptw'+version)
pt_settings = queryvalue(ptob, 'Settings_Directory')
