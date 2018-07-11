#! /usr/bin/env python
# -*- coding: utf-8 -*-
from src.file_content_search import FileContentSearch
import sys


__author__ = 'Stephan Tischer'
__date__ = '2018-07-11'
__version__ = '0.1.0'


if __name__ == "__main__":
    fcs = FileContentSearch(sys.argv)
    print(fcs.search())
