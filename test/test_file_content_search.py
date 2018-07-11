#! /usr/bin/env python
# -*- coding: utf-8 -*-
from src.data.search_result import SearchResult
from src.file_content_search import FileContentSearch
import unittest
import sys
import os


__author__ = 'Stephan Tischer'
__date__ = '2018-07-11'
__version__ = '0.1.0'


class TestFCS(unittest.TestCase):
    def test__remove_filename_from_argv__script_name_in_args__remove(self):
        # Arrange
        args = ["fcs.py", "arg1", "arg2"]

        # Act
        result = FileContentSearch._remove_main_file_from_args(args)

        # Assert
        self.assertNotIn(args[0], result)
        self.assertIn(args[1], result)
        self.assertIn(args[2], result)

    def test__remove_filename_from_argv__exe_name_in_args__remove(self):
        # Arrange
        args = ["fcs.exe", "arg1", "arg2"]

        # Act
        result = FileContentSearch._remove_main_file_from_args(args)

        # Assert
        self.assertNotIn(args[0], result)
        self.assertIn(args[1], result)
        self.assertIn(args[2], result)

    def test__shorten_path__expanded_path__remove_beginning(self):
        # Arrange
        base = os.path.join("C:/", "My", "Path")
        path = os.path.join("C:/", "My", "Path", "Sub", "MyFile.txt")
        fcs = FileContentSearch(['term', '-d', base])

        # Act
        result = fcs._shorten_path(path)

        # Assert
        self.assertEqual(os.path.join("Sub", "MyFile.txt"), result)

    def test__shorten_path__other_path__keep_beginning(self):
        # Arrange
        base = os.path.join("C:/", "My", "Path")
        path = os.path.join("D:/", "My", "Path", "Sub", "MyFile.txt")
        fcs = FileContentSearch(['term', '-d', base])

        # Act
        result = fcs._shorten_path(path)

        # Assert
        self.assertEqual(path, result)

    def test__shorten_path__option_not_set__keep_beginning(self):
        # Arrange
        base = os.path.join("C:/", "My", "Path")
        path = os.path.join("C:/", "My", "Path", "Sub", "MyFile.txt")
        fcs = FileContentSearch(['term', '-d', base, '--long'])

        # Act
        result = fcs._shorten_path(path)

        # Assert
        self.assertEqual(path, result)

    def test__group_search_results__valid_results__group(self):
        # Arrange
        base = os.path.join("C:/", "My", "Path")
        sr1 = SearchResult(os.path.join(base, "MyFile.txt"), "term1", 10)
        sr2 = SearchResult(os.path.join(base, "MyFile.txt"), "term1", 20)
        sr3 = SearchResult(os.path.join(base, "OtherFile.txt"), "term1", 11)
        sr4 = SearchResult(os.path.join(base, "sub", "MyFile.txt"), "term1", 12)
        sr5 = SearchResult(os.path.join(base, "sub", "OtherFile.txt"), "term2", 13)
        sr6 = SearchResult(os.path.join(base, "sub2", "MyFile.txt"), "term2", 14)
        sr7 = SearchResult(os.path.join(base, "sub2", "OtherFile.txt"), "term3", 15)
        sr8 = SearchResult(os.path.join(base, "sub2", "OtherFile.txt"), "term3", 25)
        input_res = [sr1, sr2, sr3, sr4, sr5, sr6, sr7, sr8]
        output_res = {
            'term1': {
                os.path.join(base, "MyFile.txt"): [10, 20],
                os.path.join(base, "OtherFile.txt"): [11],
                os.path.join(base, "sub", "MyFile.txt"): [12]
            },
            'term2': {
                os.path.join(base, "sub", "OtherFile.txt"): [13],
                os.path.join(base, "sub2", "MyFile.txt"): [14]
            },
            'term3': {
                os.path.join(base, "sub2", "OtherFile.txt"): [15, 25]
            }
        }
        fcs = FileContentSearch(['term', '-d', base])

        # Act
        result = fcs._group_search_results(input_res)

        # Assert
        self.assertEqual(output_res, result)

    def test__group_search_results__valid_results__filter_duplicated_lines(self):
        # Arrange
        base = os.path.join("C:/", "My", "Path")
        sr1 = SearchResult(os.path.join(base, "MyFile.txt"), "term1", 10)
        sr2 = SearchResult(os.path.join(base, "MyFile.txt"), "term1", 10)
        sr3 = SearchResult(os.path.join(base, "OtherFile.txt"), "term1", 11)
        sr4 = SearchResult(os.path.join(base, "sub", "MyFile.txt"), "term1", 12)
        sr5 = SearchResult(os.path.join(base, "sub", "OtherFile.txt"), "term2", 13)
        sr6 = SearchResult(os.path.join(base, "sub2", "MyFile.txt"), "term2", 14)
        sr7 = SearchResult(os.path.join(base, "sub2", "OtherFile.txt"), "term3", 15)
        sr8 = SearchResult(os.path.join(base, "sub2", "OtherFile.txt"), "term3", 25)
        input_res = [sr1, sr2, sr3, sr4, sr5, sr6, sr7, sr8]
        output_res = {
            'term1': {
                os.path.join(base, "MyFile.txt"): [10],
                os.path.join(base, "OtherFile.txt"): [11],
                os.path.join(base, "sub", "MyFile.txt"): [12]
            },
            'term2': {
                os.path.join(base, "sub", "OtherFile.txt"): [13],
                os.path.join(base, "sub2", "MyFile.txt"): [14]
            },
            'term3': {
                os.path.join(base, "sub2", "OtherFile.txt"): [15, 25]
            }
        }
        fcs = FileContentSearch(['term', '-d', base])

        # Act
        result = fcs._group_search_results(input_res)

        # Assert
        self.assertEqual(output_res, result)

    def test__group_search_results__valid_results_without_line__group(self):
        # Arrange
        base = os.path.join("C:/", "My", "Path")
        sr1 = SearchResult(os.path.join(base, "MyFile.txt"), "term1", None)
        sr2 = SearchResult(os.path.join(base, "MyFile.txt"), "term1", None)
        sr3 = SearchResult(os.path.join(base, "OtherFile.txt"), "term1", None)
        sr4 = SearchResult(os.path.join(base, "sub", "MyFile.txt"), "term1", None)
        sr5 = SearchResult(os.path.join(base, "sub", "OtherFile.txt"), "term2", None)
        sr6 = SearchResult(os.path.join(base, "sub2", "MyFile.txt"), "term2", None)
        sr7 = SearchResult(os.path.join(base, "sub2", "OtherFile.txt"), "term3", None)
        sr8 = SearchResult(os.path.join(base, "sub2", "OtherFile.txt"), "term3", None)
        input_res = [sr1, sr2, sr3, sr4, sr5, sr6, sr7, sr8]
        output_res = {
            'term1': {
                os.path.join(base, "MyFile.txt"): [None],
                os.path.join(base, "OtherFile.txt"): [None],
                os.path.join(base, "sub", "MyFile.txt"): [None]
            },
            'term2': {
                os.path.join(base, "sub", "OtherFile.txt"): [None],
                os.path.join(base, "sub2", "MyFile.txt"): [None]
            },
            'term3': {
                os.path.join(base, "sub2", "OtherFile.txt"): [None]
            }
        }
        fcs = FileContentSearch(['term', '-d', base])

        # Act
        result = fcs._group_search_results(input_res)

        # Assert
        self.assertEqual(output_res, result)

    def test__group_search_results__valid_results__shorten_paths(self):
        # Arrange
        base = os.path.join("C:/", "My", "Path")
        sr1 = SearchResult(os.path.join(base, "MyFile.txt"), "term1", 10)
        sr2 = SearchResult(os.path.join(base, "MyFile.txt"), "term1", 20)
        sr3 = SearchResult(os.path.join(base, "OtherFile.txt"), "term1", 11)
        sr4 = SearchResult(os.path.join(base, "sub", "MyFile.txt"), "term1", 12)
        sr5 = SearchResult(os.path.join(base, "sub", "OtherFile.txt"), "term2", 13)
        sr6 = SearchResult(os.path.join(base, "sub2", "MyFile.txt"), "term2", 14)
        sr7 = SearchResult(os.path.join(base, "sub2", "OtherFile.txt"), "term3", 15)
        sr8 = SearchResult(os.path.join(base, "sub2", "OtherFile.txt"), "term3", 25)
        input_res = [sr1, sr2, sr3, sr4, sr5, sr6, sr7, sr8]
        output_res = {
            'term1': {
                os.path.join(base, "MyFile.txt"): [10, 20],
                os.path.join(base, "OtherFile.txt"): [11],
                os.path.join(base, "sub", "MyFile.txt"): [12]
            },
            'term2': {
                os.path.join(base, "sub", "OtherFile.txt"): [13],
                os.path.join(base, "sub2", "MyFile.txt"): [14]
            },
            'term3': {
                os.path.join(base, "sub2", "OtherFile.txt"): [15, 25]
            }
        }
        fcs = FileContentSearch(['term', '-d', base, '--long'])

        # Act
        result = fcs._group_search_results(input_res)

        # Assert
        self.assertEqual(output_res, result)

    def test__prepare_results_for_output_simple__shortend_paths(self):
        # Arrange
        base = os.path.join("C:/", "My", "Path")
        sr1 = SearchResult(os.path.join(base, "MyFile.txt"), "term1", 10)
        sr2 = SearchResult(os.path.join(base, "MyFile.txt"), "term1", 20)
        sr3 = SearchResult(os.path.join(base, "OtherFile.txt"), "term1", 11)
        sr4 = SearchResult(os.path.join(base, "sub", "MyFile.txt"), "term1", 12)
        sr5 = SearchResult(os.path.join(base, "sub", "OtherFile.txt"), "term2", 13)
        sr6 = SearchResult(os.path.join(base, "sub2", "MyFile.txt"), "term2", 14)
        sr7 = SearchResult(os.path.join(base, "sub2", "OtherFile.txt"), "term3", 15)
        sr8 = SearchResult(os.path.join(base, "sub2", "OtherFile.txt"), "term3", 25)
        input_res = [sr1, sr2, sr3, sr4, sr5, sr6, sr7, sr8]
        fcs = FileContentSearch(['term', '-d', base])

        # Act
        result = fcs._prepare_results_for_output_simple(input_res)

        # Assert
        self.assertIn("MyFile.txt", result)
        self.assertIn("OtherFile.txt", result)
        self.assertIn(os.path.join("sub", "MyFile.txt"), result)
        self.assertIn(os.path.join("sub", "OtherFile.txt"), result)
        self.assertIn(os.path.join("sub2", "MyFile.txt"), result)
        self.assertIn(os.path.join("sub2", "OtherFile.txt"), result)

    def test__prepare_results_for_output_simple__full_paths(self):
        # Arrange
        base = os.path.join("C:/", "My", "Path")
        sr1 = SearchResult(os.path.join(base, "MyFile.txt"), "term1", 10)
        sr2 = SearchResult(os.path.join(base, "MyFile.txt"), "term1", 20)
        sr3 = SearchResult(os.path.join(base, "OtherFile.txt"), "term1", 11)
        sr4 = SearchResult(os.path.join(base, "sub", "MyFile.txt"), "term1", 12)
        sr5 = SearchResult(os.path.join(base, "sub", "OtherFile.txt"), "term2", 13)
        sr6 = SearchResult(os.path.join(base, "sub2", "MyFile.txt"), "term2", 14)
        sr7 = SearchResult(os.path.join(base, "sub2", "OtherFile.txt"), "term3", 15)
        sr8 = SearchResult(os.path.join(base, "sub2", "OtherFile.txt"), "term3", 25)
        input_res = [sr1, sr2, sr3, sr4, sr5, sr6, sr7, sr8]
        fcs = FileContentSearch(['term', '-d', base, '--long'])

        # Act
        result = fcs._prepare_results_for_output_simple(input_res)

        # Assert
        self.assertIn(os.path.join(base, "MyFile.txt"), result)
        self.assertIn(os.path.join(base, "OtherFile.txt"), result)
        self.assertIn(os.path.join(base, "sub", "MyFile.txt"), result)
        self.assertIn(os.path.join(base, "sub", "OtherFile.txt"), result)
        self.assertIn(os.path.join(base, "sub2", "MyFile.txt"), result)
        self.assertIn(os.path.join(base, "sub2", "OtherFile.txt"), result)

    def test__prepare_results_for_output_complex_shortend_paths(self):
        # Arrange
        base = os.path.join("C:/", "My", "Path")
        sr1 = SearchResult(os.path.join(base, "MyFile.txt"), "term1", 10)
        sr2 = SearchResult(os.path.join(base, "MyFile.txt"), "term1", 20)
        sr3 = SearchResult(os.path.join(base, "OtherFile.txt"), "term1", 11)
        sr4 = SearchResult(os.path.join(base, "sub", "MyFile.txt"), "term1", 12)
        sr5 = SearchResult(os.path.join(base, "sub", "OtherFile.txt"), "term2", 13)
        sr6 = SearchResult(os.path.join(base, "sub2", "MyFile.txt"), "term2", 14)
        sr7 = SearchResult(os.path.join(base, "sub2", "OtherFile.txt"), "term3", 15)
        sr8 = SearchResult(os.path.join(base, "sub2", "OtherFile.txt"), "term3", 25)
        input_res = [sr1, sr2, sr3, sr4, sr5, sr6, sr7, sr8]
        fcs = FileContentSearch(['term', '-d', base])

        # Act
        result = fcs._prepare_results_for_output_complex(input_res)

        # Assert
        self.assertIn("MyFile.txt", result)
        self.assertIn("OtherFile.txt", result)
        self.assertIn(os.path.join("sub", "MyFile.txt"), result)
        self.assertIn(os.path.join("sub", "OtherFile.txt"), result)
        self.assertIn(os.path.join("sub2", "MyFile.txt"), result)
        self.assertIn(os.path.join("sub2", "OtherFile.txt"), result)

    def test__prepare_results_for_output_complex__full_paths(self):
        # Arrange
        base = os.path.join("C:/", "My", "Path")
        sr1 = SearchResult(os.path.join(base, "MyFile.txt"), "term1", 10)
        sr2 = SearchResult(os.path.join(base, "MyFile.txt"), "term1", 20)
        sr3 = SearchResult(os.path.join(base, "OtherFile.txt"), "term1", 11)
        sr4 = SearchResult(os.path.join(base, "sub", "MyFile.txt"), "term1", 12)
        sr5 = SearchResult(os.path.join(base, "sub", "OtherFile.txt"), "term2", 13)
        sr6 = SearchResult(os.path.join(base, "sub2", "MyFile.txt"), "term2", 14)
        sr7 = SearchResult(os.path.join(base, "sub2", "OtherFile.txt"), "term3", 15)
        sr8 = SearchResult(os.path.join(base, "sub2", "OtherFile.txt"), "term3", 25)
        input_res = [sr1, sr2, sr3, sr4, sr5, sr6, sr7, sr8]
        fcs = FileContentSearch(['term', '-d', base, '--long'])

        # Act
        result = fcs._prepare_results_for_output_complex(input_res)

        # Assert
        self.assertIn(os.path.join(base, "MyFile.txt"), result)
        self.assertIn(os.path.join(base, "OtherFile.txt"), result)
        self.assertIn(os.path.join(base, "sub", "MyFile.txt"), result)
        self.assertIn(os.path.join(base, "sub", "OtherFile.txt"), result)
        self.assertIn(os.path.join(base, "sub2", "MyFile.txt"), result)
        self.assertIn(os.path.join(base, "sub2", "OtherFile.txt"), result)

    def test__search__no_exception(self):
        # Arrange
        fcs = FileContentSearch(['def', '-d', '.'])

        # Act & Assert
        try:
            fcs.search()
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test__search__simple_search__result_string(self):
        # Arrange
        fcs = FileContentSearch(['def', '-d', '.'])

        # Act
        result = fcs.search()

        # Assert
        self.assertTrue(isinstance(result, str))

    def test__search__complex_search__result_string(self):
        # Arrange
        fcs = FileContentSearch(['def', '-l', '-d', '.'])

        # Act
        result = fcs.search()

        # Assert
        self.assertTrue(isinstance(result, str))
