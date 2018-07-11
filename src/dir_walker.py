#! /usr/bin/env python
# -*- coding: utf-8 -*-
from .data.file import File
import os


__author__ = 'Stephan Tischer'
__date__ = '2018-07-10'
__version__ = '0.1.0'


class DirWalker:
    """
    Functionality to walk through directories and read file content
    """

    _allowed_extensions = None
    _search_recursive = True

    @staticmethod
    def is_directory(path: str) -> bool:
        """ Checks if given path leads to file or directory

        :param path: Path to check
        :return: Return TRUE if target is directory, otherwise false
        """

        if not os.path.exists(path):
            return False
        return os.path.isdir(path)

    def __init__(self):
        """ Init default instance """

        pass

    def __init__(self, allowed_extensions=None, recursive=True):
        """ Init with presets

        :param allowed_extensions: List with extensions to include in search results
        :param recursive: Search subdirectories
        """

        self.set_allowed_extensions(allowed_extensions)
        self.set_search_recursive(recursive)

    def set_allowed_extensions(self, extensions: list):
        """ Set extensions which should be included in search results

        :param extensions: List with extensions to include in search results
        """

        if extensions is None:
            self._allowed_extensions = None
        else:
            if not isinstance(extensions, list):
                extensions = [extensions]

            if len(extensions) == 0:
                self._allowed_extensions = None
            else:
                self._allowed_extensions = extensions

    def set_search_recursive(self, recursive: bool):
        """ Set to TRUE if all subdirectories should also be searched

        :param recursive: Search subdirectories
        """

        if not isinstance(recursive, bool):
            self._search_recursive = True
        else:
            self._search_recursive = recursive

    def has_allowed_extension(self, file: str) -> bool:
        """ Checks if a given file should be included in the search results, because of the extension

        :param file: Name or full path of the file to check
        :return: Returns TRUE if file is allowed, otherwise FALSE
        """

        if self._allowed_extensions is None:
            return True

        for ext in self._allowed_extensions:
            if file.endswith(ext):
                return True
        return False

    def list_files(self, path: str) -> list:
        """ Lists all files which are saved under the given path

        :param path: Path for directory to check
        :return: List with all files
        """

        files = list()
        if os.path.exists(path):
            for f in os.listdir(path):
                if DirWalker.is_directory(os.path.join(path, f)):
                    if self._search_recursive:
                        files += self.list_files(os.path.join(path, f))
                elif self.has_allowed_extension(f):
                    files.append(
                        File(os.path.join(path, f))
                    )
        return files
