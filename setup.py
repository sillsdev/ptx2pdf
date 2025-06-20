#!/usr/bin/python3

from setuptools import setup
from setuptools.command.build_py import build_py
import os, shutil

class CustomBuild(build_py):
    def run(self):

        super().run()
        # copy data dirs into the build tree
        for a in (("src", "ptx2pdf"), ("xetex", "xetex")):
            src = os.path.abspath(a[0])
            tgt = os.path.join(self.build_lib, "ptxprint", a[1])
            if os.path.exists(tgt):
                shutil.rmtree(tgt)
            shutil.copytree(src, tgt)
        shutil.rmtree(os.path.join(self.build_lib, "ptxprint", "xetex", "bin"))

setup(
    cmdclass = {'build_py': CustomBuild}    # runs after module discovery
)

