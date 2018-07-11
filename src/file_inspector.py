#! /usr/bin/env python
# -*- coding: utf-8 -*-
from .data.search_result import SearchResult
import concurrent.futures
import os


__author__ = 'Stephan Tischer'
__date__ = '2018-07-10'
__version__ = '0.1.0'


class FileInspector:
    """
    Processes file content to search for terms
    """

    @staticmethod
    def read_file(path: str) -> str:
        """ Read whole file at once and return content as string

        :param path: Path to file
        :return: Content as string
        """

        if not os.path.exists(path) or not os.path.isfile(path):
            return ""

        content = ""
        with open(path, 'r', errors='ignore') as fh:
            for line in fh.readlines():
                content += line
        return content

    @staticmethod
    def get_numbers_of_lines(content: str, offset=0) -> int:
        """ Calculates the number of lines in the given string

        :param content: String to count lines in
        :param offset: Offset to add to the result
        :return: Number of lines
        """

        return content.count("\n") + 1 + offset

    @staticmethod
    def split_content(content: str, pos: int) -> tuple:
        """ Split content into two paths at the given position

        :param content: Content to split
        :param pos: Position to split content at (-1 = don't split, move everything into first part)
        :return: Returns tuple containing the both results of the split
        """

        if pos != -1:
            return content[:pos], content[pos:]
        return content, ""

    @staticmethod
    def exec_simple_search(path: str, content: str, term: str) -> list:
        """ Execute a simple search in the given content

        :param path: Path to file (only needed to create complete SearchResult
        :param content: Content to search through
        :param term: String to search for
        :return: Returns a list with all SearchResults
        """

        if term in content:
            return [SearchResult(path, term, None), ]
        return list()

    @staticmethod
    def exec_search_show_lines(path: str, content: str, term: str) -> list:
        """ Execute a search also tracking lines in which the term was found

        :param path: Path to file (only needed to create complete SearchResult
        :param content: Content to search through
        :param term: String to search for
        :return: Returns a list with all SearchResults
        """

        results = list()
        cur_content = content
        len_break = len("\n")
        line_number = 0

        pos_term = cur_content.find(term)
        pos_break = cur_content.find("\n", pos_term)
        while pos_term != -1:
            # Split content
            if pos_break != -1:
                until_term, cur_content = FileInspector.split_content(cur_content, pos_break + len_break)
                # Remove last line break for correct calculation of lines
                until_term = until_term[:-len_break]
            else:
                until_term, cur_content = FileInspector.split_content(cur_content, -1)

            # If term also has line break, get line number with start of term
            line_number = FileInspector.get_numbers_of_lines(until_term, line_number)
            results.append(SearchResult(path, term, line_number))

            # Search for next one
            pos_term = cur_content.find(term)
            pos_break = cur_content.find("\n", pos_term)

        return results

    @staticmethod
    def search_worker(path: str, terms: list, case_sensitive=False, show_lines=False) -> list:
        """ Searches in the given file for the given terms

        :param path: Path to file
        :param terms: Search terms
        :param case_sensitive: Search is case sensitive
        :param show_lines: Track lines of appearance
        :return: List with search results
        """

        results = list()
        content = FileInspector.read_file(path)

        if not isinstance(terms, list):
            terms = [terms]

        if not case_sensitive:
            content = content.lower()

        for term in terms:
            if not case_sensitive:
                term = term.lower()

            if show_lines:
                results += FileInspector.exec_search_show_lines(path, content, term)
            else:
                results += FileInspector.exec_simple_search(path, content, term)

        return results

    @staticmethod
    def inspect_files(paths: list, terms: list, case_sensitive=False, show_lines=False) -> list:
        """ Inspect multiple files

        :param paths: Paths to files
        :param terms: Terms to search for
        :param case_sensitive: Search is case sensitive
        :param show_lines: Track lines of appearance
        :return: List with all hits
        """

        results = list()

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            # Execute workers async
            workers = {
                executor.submit(FileInspector.search_worker, path, terms, case_sensitive, show_lines):
                    path for path in paths
            }

            for worker_completed in concurrent.futures.as_completed(workers):
                try:
                    results += worker_completed.result()
                except Exception as ex:
                    print("\nException in Worker:")
                    print(ex)

        return sorted(results)
