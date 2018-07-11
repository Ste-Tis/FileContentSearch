#! /usr/bin/env python
# -*- coding: utf-8 -*-
from .file_inspector import FileInspector
from .dir_walker import DirWalker
from .cmd_parser import CmdParser
import sys


__author__ = 'Stephan Tischer'
__date__ = '2018-07-11'
__version__ = '0.1.0'


class FileContentSearch:
    """
    Start and manage search
    """

    def __init__(self, args):
        """ Init search

        :param args: Commandline parameter
        """

        self.config = CmdParser.parse(self._remove_main_file_from_args(args))

    @staticmethod
    def _remove_main_file_from_args(argv):
        """ Removes the name of the main file from commandline arguments

        :param argv: Commandline arguments
        :return: Cleaned up list
        """

        if 'fcs.exe' in argv[0] or 'fcs.py' in argv[0]:
            return argv[1:]
        return argv

    def _shorten_path(self, path: str) -> str:
        """ Remove base path from paths to files

        Without:
            C:/My/Path/src/MyFile.txt
        With:
            src/MyFile.txt

        :param path: Path to shorten
        :return: Shortened path
        """

        if not self.config.long and path.startswith(self.config.dir):
            shorten = len(self.config.dir)
            if not (self.config.dir.endswith('/') or self.config.dir.endswith('\\')):
                shorten += 1
            path = path[shorten:]
        return path

    @staticmethod
    def _group_search_results(results: list) -> dict:
        """ Group results by term and file

        :param results: Search results
        :return: Grouped results
        """

        grouped_results = dict()
        for r in results:
            if r.term not in grouped_results:
                grouped_results[r.term] = {}
            if r.file not in grouped_results[r.term]:
                grouped_results[r.term][r.file] = []
            if r.line_number not in grouped_results[r.term][r.file]:
                grouped_results[r.term][r.file].append(r.line_number)
        return grouped_results

    def _prepare_results_for_output_simple(self, results: list):
        """ Print search results for simple search without line numbers

        :param results: List with search results
        :return: String with formatted results
        """

        result_str = ""

        grouped_results = self._group_search_results(results)
        for term in sorted(grouped_results):
            result_str += "\n>> %s\n" % term
            for file in grouped_results[term]:
                result_str += "  %s\n" % self._shorten_path(file)
        return result_str

    def _prepare_results_for_output_complex(self, results: list):
        """ Print search results for complex search with line numbers

        :param results: List with search results
        :return: String with formatted results
        """

        result_str = ""

        grouped_results = self._group_search_results(results)
        for term in sorted(grouped_results):
            result_str += "\n>> %s\n" % term
            for file in grouped_results[term]:
                result_str += "  %s\n      [%s]\n" % (
                    self._shorten_path(file),
                    ', '.join(str(x) for x in grouped_results[term][file])
                )
        return result_str

    def search(self) -> str:
        """ Start search. Prints results to console.

        :return: Returns results as formatted string
        """

        res_string = "Searching in %s for %s:\n" % (self.config.dir, self.config.search)

        dw = DirWalker()
        dw.set_search_recursive(self.config.recursive)
        dw.set_allowed_extensions(self.config.extensions)

        results = FileInspector.inspect_files(
            [x.path for x in dw.list_files(self.config.dir)],
            self.config.search,
            self.config.case_sensitive,
            self.config.lines
        )

        if self.config.lines:
            res_string += self._prepare_results_for_output_complex(results)
        else:
            res_string += self._prepare_results_for_output_simple(results)

        return res_string
