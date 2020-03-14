#!/usr/bin/env python3

from distutils.core import setup
from glob import glob

setup(name="PtxPrint",
        version = "0.1",
        description = "Typesetting using tex for paratext",
        packages = ['ptxprint'],
        package_dir = {'': 'lib'},
        scripts = ['scripts/ptxprint'],
        package_data = {'ptxprint': ['*.pdf', 'ptxprint.glade', 'template.tex',
                            'mappings/*.tec', 'mappings/*.map']},
        data_files = [('ptx2pdf', glob('../src/*.tex'))]
    )
