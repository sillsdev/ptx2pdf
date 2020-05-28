#!/usr/bin/python3
""" py3.8 Ubuntu focal test packaging """

from setuptools import setup, find_packages

setup(
    name="PTXprint",
    version="0.7.0",
    description="Typesetting using (Xe)TeX for ParaText",
    url="https://software.sil.org/ptxprint",
    maintainer="SIL International",
    packages=find_packages('lib'),  # include all packages under lib
    package_dir={'': 'lib'},  # indicate packages are under lib
    include_package_data=True,  # include everything in MANIFEST.in
    package_data={'ptxprint': ['*.*']},
    scripts=["scripts/ptxprint"],
    install_requires=["regex", "pygobject", "img2pdf", "fonttools", "pycairo"],
    zip_safe=False,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: X11 Applications :: GTK",
        "Topic :: Text Editors :: Text Processing",
        "License :: OSI Approved :: MIT License",
    ]
)
