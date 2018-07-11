#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os.path

__author__ = 'Stephan Tischer'
__date__ = '2018-07-10'
__version__ = '0.1.0'


class File:
    """
    Store all needed information for an file
    """

    name: str
    path: str
    extension: str

    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.extension = os.path.splitext(path)[1].replace('.', '').lower()

    def __lt__(self, other):
        if not isinstance(other, File):
            return False
        return self.name < other.name

    def __gt__(self, other):
        if not isinstance(other, File):
            return True
        return self.name > other.name

    def __eq__(self, other):
        if not isinstance(other, File):
            return False
        return self.path == other.path

    def __ne__(self, other):
        if not isinstance(other, File):
            return True
        return self.path != other.path

    def __str__(self):
        return "File(Name: %s; Path: %s; Extension: %s)" % (self.name, self.path, self.extension)

    def __repr__(self):
        return self.__str__()
