#! /usr/bin/env python
# -*- coding: utf-8 -*-
from src.cmd_parser import CmdParser
import unittest
import os


__author__ = 'Stephan Tischer'
__date__ = '2018-07-07'
__version__ = '0.1.0'


class TestCmdParser(unittest.TestCase):
    def assertHasAllAttr(self, return_value):
        """
        Tests if all needed attributes are provided
        """

        self.assertTrue(hasattr(return_value, 'search'))
        self.assertTrue(hasattr(return_value, 'dir'))
        self.assertTrue(hasattr(return_value, 'extensions'))
        self.assertTrue(hasattr(return_value, 'lines'))
        self.assertTrue(hasattr(return_value, 'case_sensitive'))
        self.assertTrue(hasattr(return_value, 'long'))
        self.assertTrue(hasattr(return_value, 'recursive'))
        self.assertTrue(type(return_value.search) == list)

    def test__parse__search__one_term(self):
        # Act
        result = CmdParser.parse(['Egon Olsen'])

        # Assert
        self.assertHasAllAttr(result)
        self.assertListEqual(['Egon Olsen'], result.search)

    def test__parse__search__multiple_terms(self):
        # Arrange
        terms = ['Egon Olsen', 'Benny Frandsen', ' Kjeld Jensen']

        # Act
        result = CmdParser.parse(terms)

        # Assert
        self.assertHasAllAttr(result)
        self.assertListEqual(sorted(terms), sorted(result.search))

    def test__parse__no_dir_param(self):
        # Act
        result = CmdParser.parse(['Egon Olsen'])

        # Assert
        self.assertEqual(os.getcwd(), result.dir)

    def test__parse__dir_param_short(self):
        # Arrange
        path = os.path.join("C:", "my", "path")

        # Act
        result = CmdParser.parse(['Egon Olsen', '-d', path])

        # Assert
        self.assertHasAllAttr(result)
        self.assertEqual(path, result.dir)

    def test__parse__dir_param_long(self):
        # Arrange
        path = os.path.join("C:", "my", "path")

        # Act
        result = CmdParser.parse(['Egon Olsen', '--dir', path])

        # Assert
        self.assertHasAllAttr(result)
        self.assertEqual(path, result.dir)

    def test__parse__no_extension_param(self):
        # Act
        result = CmdParser.parse(['Egon Olsen'])

        # Assert
        self.assertHasAllAttr(result)
        self.assertIsNone(result.extensions)

    def test__parse__extension_param_short(self):
        # Arrange
        ext_in = [".txt"]
        ext_out = ["txt"]

        # Act
        result = CmdParser.parse(['Egon Olsen', '-e'] + ext_in)

        # Assert
        self.assertHasAllAttr(result)
        self.assertEqual(ext_out, result.extensions)

    def test__parse__extension_param_long(self):
        # Arrange
        ext_in = [".txt"]
        ext_out = ["txt"]

        # Act
        result = CmdParser.parse(['Egon Olsen', '--extensions'] + ext_in)

        # Assert
        self.assertHasAllAttr(result)
        self.assertEqual(ext_out, result.extensions)

    def test__parse__multiple_extension_params(self):
        # Arrange
        ext_in = ['.txt', '.css', '.py']
        ext_out = ['txt', 'css', 'py']

        # Act
        result = CmdParser.parse(['Egon Olsen', '-e'] + ext_in)

        # Assert
        self.assertHasAllAttr(result)
        self.assertListEqual(sorted(ext_out), sorted(result.extensions))

    def test__parse__extension_remove_point(self):
        # Arrange
        ext_in = ['.txt', 'css']
        ext_out = ['txt', 'css']

        # Act
        result = CmdParser.parse(['Egon Olsen', '-e'] + ext_in)

        # Assert
        self.assertHasAllAttr(result)
        self.assertListEqual(sorted(ext_out), sorted(result.extensions))

    def test__parse__no_lines_param(self):
        # Act
        result = CmdParser.parse(['Egon Olsen'])

        # Assert
        self.assertFalse(result.lines)

    def test__parse__lines_param_short(self):
        # Act
        result = CmdParser.parse(['Egon Olsen', '-l'])

        # Assert
        self.assertHasAllAttr(result)
        self.assertTrue(result.lines)

    def test__parse__lines_param_long(self):
        # Act
        result = CmdParser.parse(['Egon Olsen', '--lines'])

        # Assert
        self.assertHasAllAttr(result)
        self.assertTrue(result.lines)

    def test__parse__no_case_sensitive_param(self):
        # Act
        result = CmdParser.parse(['Egon Olsen'])

        # Assert
        self.assertFalse(result.case_sensitive)

    def test__parse__case_sensitive_param_short(self):
        # Act
        result = CmdParser.parse(['Egon Olsen', '-cs'])

        # Assert
        self.assertHasAllAttr(result)
        self.assertTrue(result.case_sensitive)

    def test__parse__case_sensitive_param_long(self):
        # Act
        result = CmdParser.parse(['Egon Olsen', '--case-sensitive'])

        # Assert
        self.assertHasAllAttr(result)
        self.assertTrue(result.case_sensitive)

    def test__parse__no_long_param(self):
        # Act
        result = CmdParser.parse(['Egon Olsen'])

        # Assert
        self.assertFalse(result.long)

    def test__parse__long_param(self):
        # Act
        result = CmdParser.parse(['Egon Olsen', '--long'])

        # Assert
        self.assertHasAllAttr(result)
        self.assertTrue(result.long)

    def test__parse__no_subdirectories_param(self):
        # Act
        result = CmdParser.parse(['Egon Olsen'])

        # Assert
        self.assertTrue(result.recursive)

    def test__parse__subdirectories_param_short(self):
        # Act
        result = CmdParser.parse(['Egon Olsen', '-ns'])

        # Assert
        self.assertHasAllAttr(result)
        self.assertFalse(result.recursive)

    def test__parse__subdirectories_param_long(self):
        # Act
        result = CmdParser.parse(['Egon Olsen', '--no-subdirectories'])

        # Assert
        self.assertHasAllAttr(result)
        self.assertFalse(result.recursive)
