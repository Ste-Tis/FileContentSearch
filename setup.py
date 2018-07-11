#! /usr/bin/env python
# -*- coding: utf-8 -*-
from cx_Freeze import setup, Executable


__author__ = 'Stephan Tischer'
__date__ = '2018-07-11'
__version__ = '0.1.0'


base = None

executables = [Executable('fcs.py', base=base)]
packages = []
options = {
    'build_exe': {
        'packages': packages
    }
}

setup(
    name='FileContentSearch',
    options=options,
    version='0.1.0',
    description='Search the content of every file in a directory for the appearance of a term',
    executables=executables
)
