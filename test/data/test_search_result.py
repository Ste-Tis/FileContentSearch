#! /usr/bin/env python
# -*- coding: utf-8 -*-
from src.data.search_result import SearchResult
import unittest
import os


__author__ = 'Stephan Tischer'
__date__ = '2018-07-10'
__version__ = '0.1.0'


class TestSearchResult(unittest.TestCase):
    def test__search_result__setting_values(self):
        # Act
        f = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'SearchTerm', 10)

        # Assert
        self.assertEqual(os.path.join('C:', 'my', 'path', 'theFile.txt'), f.file)
        self.assertEqual('SearchTerm', f.term)
        self.assertEqual(10, f.line_number)

    def test__comparision__lt_file(self):
        # Arrange
        f_a = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'SearchTerm', 10)
        f_b = SearchResult(os.path.join('D:', 'my', 'path', 'theFile.txt'), 'SearchTerm', 10)

        # Act
        result = f_a < f_b

        # Arrange
        self.assertTrue(result)

    def test__comparision__lt_line_number(self):
        # Arrange
        f_a = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'SearchTerm', 10)
        f_b = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'SearchTerm', 12)

        # Act
        result = f_a < f_b

        # Arrange
        self.assertTrue(result)

    def test__comparision__lt_term(self):
        # Arrange
        f_a = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'A', 10)
        f_b = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'B', 10)

        # Act
        result = f_a < f_b

        # Arrange
        self.assertTrue(result)

    def test__comparision__not_lt(self):
        # Arrange
        f_a = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'B', 10)
        f_b = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'A', 10)

        # Act
        result = f_a < f_b

        # Arrange
        self.assertFalse(result)

    def test__comparision__lt_other_object(self):
        # Arrange
        f_a = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'B', 10)
        f_b = "other object"

        # Act
        result = f_a < f_b

        # Arrange
        self.assertFalse(result)

    def test__comparision__gt_file(self):
        # Arrange
        f_a = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'SearchTerm', 10)
        f_b = SearchResult(os.path.join('D:', 'my', 'path', 'theFile.txt'), 'SearchTerm', 10)

        # Act
        result = f_a > f_b

        # Arrange
        self.assertFalse(result)

    def test__comparision__gt_line_number(self):
        # Arrange
        f_a = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'SearchTerm', 10)
        f_b = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'SearchTerm', 12)

        # Act
        result = f_a > f_b

        # Arrange
        self.assertFalse(result)

    def test__comparision__gt_term(self):
        # Arrange
        f_a = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'A', 10)
        f_b = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'B', 10)

        # Act
        result = f_a > f_b

        # Arrange
        self.assertFalse(result)

    def test__comparision__not_gt(self):
        # Arrange
        f_a = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'A', 10)
        f_b = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'B', 10)

        # Act
        result = f_a > f_b

        # Arrange
        self.assertFalse(result)

    def test__comparision__gt_other_object(self):
        # Arrange
        f_a = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'B', 10)
        f_b = "other object"

        # Act
        result = f_a > f_b

        # Arrange
        self.assertTrue(result)

    def test__comparision__eq(self):
        # Arrange
        f_a = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'SearchTerm', 10)

        # Act
        result = f_a == f_a

        # Arrange
        self.assertTrue(result)

    def test__comparision__not_eq(self):
        # Arrange
        f_a = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'SearchTerm', 10)
        f_b = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'SearchTerm', 20)

        # Act
        result = f_a == f_b

        # Arrange
        self.assertFalse(result)

    def test__comparision__eq_other_object(self):
        # Arrange
        f_a = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'SearchTerm', 10)
        f_b = "other object"

        # Act
        result = f_a == f_b

        # Arrange
        self.assertFalse(result)

    def test__comparision__ne(self):
        # Arrange
        f_a = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'B', 10)
        f_b = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'A', 10)

        # Act
        result = f_a != f_b

        # Arrange
        self.assertTrue(result)

    def test__comparision__not_ne(self):
        # Arrange
        f_a = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'A', 10)
        f_b = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'A', 10)

        # Act
        result = f_a != f_b

        # Arrange
        self.assertFalse(result)

    def test__comparision__ne_other_object(self):
        # Arrange
        f_a = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'A', 10)
        f_b = "other object"

        # Act
        result = f_a != f_b

        # Arrange
        self.assertTrue(result)

    def test__comparision__repr(self):
        # Arrange
        f = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'B', 10)

        # Act
        result = f.__repr__()

        # Arrange
        self.assertEqual(str, type(result))

    def test__comparision__str(self):
        # Arrange
        f = SearchResult(os.path.join('C:', 'my', 'path', 'theFile.txt'), 'B', 10)

        # Act
        result = str(f)

        # Arrange
        self.assertEqual(str, type(result))
