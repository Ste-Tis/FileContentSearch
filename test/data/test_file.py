#! /usr/bin/env python
# -*- coding: utf-8 -*-
from src.data.file import File
import unittest
import os


__author__ = 'Stephan Tischer'
__date__ = '2018-07-10'
__version__ = '0.1.0'


class TestFiles(unittest.TestCase):
    def test__file__setting_values(self):
        # Act
        f = File(os.path.join('C:', 'my', 'path', 'theFile.txt'))

        # Assert
        self.assertEqual(os.path.join('C:', 'my', 'path', 'theFile.txt'), f.path)
        self.assertEqual('theFile.txt', f.name)
        self.assertEqual('txt', f.extension)

    def test__comparison__lt(self):
        # Arrange
        f_a = File(os.path.join('C:', 'my', 'path', 'a.txt'))
        f_b = File(os.path.join('C:', 'my', 'path', 'b.txt'))

        # Act
        result = f_a < f_b

        # Arrange
        self.assertTrue(result)

    def test__comparison__not_lt(self):
        # Arrange
        f_a = File(os.path.join('C:', 'my', 'path', 'b.txt'))
        f_b = File(os.path.join('C:', 'my', 'path', 'a.txt'))

        # Act
        result = f_a < f_b

        # Arrange
        self.assertFalse(result)

    def test__comparison__lt_other_object(self):
        # Arrange
        f_a = File(os.path.join('C:', 'my', 'path', 'b.txt'))
        f_b = "other object"

        # Act
        result = f_a < f_b

        # Arrange
        self.assertFalse(result)

    def test__comparison__gt(self):
        # Arrange
        f_a = File(os.path.join('C:', 'my', 'path', 'b.txt'))
        f_b = File(os.path.join('C:', 'my', 'path', 'a.txt'))

        # Act
        result = f_a > f_b

        # Arrange
        self.assertTrue(result)

    def test__comparison__not_gt(self):
        # Arrange
        f_a = File(os.path.join('C:', 'my', 'path', 'a.txt'))
        f_b = File(os.path.join('C:', 'my', 'path', 'b.txt'))

        # Act
        result = f_a > f_b

        # Arrange
        self.assertFalse(result)

    def test__comparison__gt_other_object(self):
        # Arrange
        f_a = File(os.path.join('C:', 'my', 'path', 'a.txt'))
        f_b = "other object"

        # Act
        result = f_a > f_b

        # Arrange
        self.assertTrue(result)

    def test__comparison__eq(self):
        # Arrange
        f_a = File(os.path.join('C:', 'my', 'path', 'a.txt'))

        # Act
        result = f_a == f_a

        # Arrange
        self.assertTrue(result)

    def test__comparison__not_eq(self):
        # Arrange
        f_a = File(os.path.join('C:', 'my', 'path', 'a.txt'))
        f_b = File(os.path.join('C:', 'my', 'path', 'b.txt'))

        # Act
        result = f_a == f_b

        # Arrange
        self.assertFalse(result)

    def test__comparison__eq_other_object(self):
        # Arrange
        f_a = File(os.path.join('C:', 'my', 'path', 'a.txt'))
        f_b = "other object"

        # Act
        result = f_a == f_b

        # Arrange
        self.assertFalse(result)

    def test__comparison__ne(self):
        # Arrange
        f_a = File(os.path.join('C:', 'my', 'path', 'a.txt'))
        f_b = File(os.path.join('C:', 'my', 'path', 'b.txt'))

        # Act
        result = f_a != f_b

        # Arrange
        self.assertTrue(result)

    def test__comparison__not_ne(self):
        # Arrange
        f_a = File(os.path.join('C:', 'my', 'path', 'a.txt'))
        f_b = File(os.path.join('C:', 'my', 'path', 'a.txt'))

        # Act
        result = f_a != f_b

        # Arrange
        self.assertFalse(result)

    def test__comparison__ne__other_object(self):
        # Arrange
        f_a = File(os.path.join('C:', 'my', 'path', 'a.txt'))
        f_b = "other object"

        # Act
        result = f_a != f_b

        # Arrange
        self.assertTrue(result)

    def test__comparison__repr(self):
        # Arrange
        f = File(os.path.join('C:', 'my', 'path', 'a.txt'))

        # Act
        result = f.__repr__()

        # Arrange
        self.assertEqual(str, type(result))

    def test__comparison__str(self):
        # Arrange
        f = File(os.path.join('C:', 'my', 'path', 'a.txt'))

        # Act
        result = str(f)

        # Arrange
        self.assertEqual(str, type(result))
