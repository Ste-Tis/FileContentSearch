#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Stephan Tischer'
__date__ = '2018-07-11'
__version__ = '0.1.0'


class SearchResult:
    """
    Stores all information to an search result
    """

    file: str
    term: str
    line_number: int

    def __init__(self, file, term, line_number):
        self.file = file
        self.term = term
        self.line_number = line_number

    def __lt__(self, other):
        if not isinstance(other, SearchResult):
            return False

        if self.file < other.file:
            return True
        if self.file == other.file:
            if self.term < other.term:
                return True
            if self.term == other.term and self.line_number < other.line_number:
                return True
        return False

    def __gt__(self, other):
        if not isinstance(other, SearchResult):
            return True

        if self.file > other.file:
            return True
        if self.file == other.file:
            if self.term > other.term:
                return True
            if self.term == other.term and self.line_number > other.line_number:
                return True
        return False

    def __eq__(self, other):
        if not isinstance(other, SearchResult):
            return False
        return self.file == other.file and self.line_number == other.line_number and self.term == other.term

    def __ne__(self, other):
        if not isinstance(other, SearchResult):
            return True
        return self.file != other.file or self.line_number != other.line_number or self.term != other.term

    def __str__(self):
        return "SearchResult(File: %s; Term: %s; Line: %s)" % (self.file, self.term, self.line_number)

    def __repr__(self):
        return self.__str__()
