#!/usr/bin/python3

from glob import glob
from setuptools import setup, find_packages

setup(
    name="PTXprint",
    version="2.7.35",
    description="Typesetting using (Xe)TeX for Paratext",
    url="https://software.sil.org/ptxprint",
    author="SIL International",
    packages=find_packages('python/lib'),  # include all packages under lib
    package_dir={'': 'python/lib'},  # indicate packages are under lib
    include_package_data=True,  # include everything in MANIFEST.in
    package_data={'ptxprint': ['*.*']},
    scripts=["python/scripts/ptxprint", "python/scripts/xdvitype", "python/scripts/pdfdiff"],
    install_requires=["regex", "pygobject", "fonttools", "pycairo", "appdirs", "Pillow", "numpy"], #, "ssl"],
    zip_safe=False,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: X11 Applications :: GTK",
        "Topic :: Text Editors :: Text Processing",
        "License :: OSI Approved :: MIT License",
    ]
)
