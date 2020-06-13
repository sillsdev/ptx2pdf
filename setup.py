#!/usr/bin/python3
""" py3.8 Ubuntu focal test packaging """

from glob import glob
from setuptools import setup, find_packages

setup(
    name="PTXprint",
    version="0.8.1",
    description="Typesetting using (Xe)TeX for ParaText",
    url="https://software.sil.org/ptxprint",
    maintainer="SIL International",
    packages=find_packages('python/lib'),  # include all packages under lib
    package_dir={'': 'python/lib'},  # indicate packages are under lib
    include_package_data=True,  # include everything in MANIFEST.in
    package_data={'ptxprint': ['*.*']},
    #data_files=[('ptx2pdf/src', glob('src/*.tex')),
    #            ('ptx2pdf/src/mappings', glob('src/mappings/*.tec'))],
    scripts=["python/scripts/ptxprint", "python/scripts/xdvitype"],
    install_requires=["regex", "pygobject", "fonttools", "pycairo"],
    zip_safe=False,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: X11 Applications :: GTK",
        "Topic :: Text Editors :: Text Processing",
        "License :: OSI Approved :: MIT License",
    ]
)
