#! /usr/bin/env python
# -*- coding: utf-8 -*-
from src.dir_walker import File, DirWalker
import tempfile
import unittest
import shutil
import os


__author__ = 'Stephan Tischer'
__date__ = '2018-07-10'
__version__ = '0.1.0'


class TestDirWalker(unittest.TestCase):
    def setUp(self):
        """
        Create real directories and files, because mocking recursive calls is a pain in the ass
        """

        self.cur_path = tempfile.gettempdir()
        self.root_path = os.path.join(self.cur_path, 'root')
        self.sub1_path = os.path.join(self.root_path, 'sub1')
        self.sub2_path = os.path.join(self.root_path, 'sub2')
        self.txt_path = os.path.join(self.root_path, 'lorem.txt')
        self.py_path = os.path.join(self.sub1_path, 'amon.py')
        self.log_path = os.path.join(self.sub1_path, 'amarth.log')

        txt_content = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr,\n" \
                      "sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,\n" \
                      "sed diam voluptua."
        py_content = "#! /usr/bin/env python\n" \
                     "# -*- coding: utf-8 -*-\n" \
                     "from dataclasses import dataclass\n" \
                     "import os\n" \
                     "\n\n" \
                     "__author__ = 'Stephan Tischer'\n" \
                     "__date__ = '2018-07-04'\n" \
                     "__version__ = '0.1.0'\n" \
                     "\n\n" \
                     "@dataclass\n" \
                     "class File:\n" \
                     "  name: str\n" \
                     "  path: str\n" \
                     "  extension: str\n" \
                     "\n\n" \
                     "  def __init__(self, path):\n" \
                     "      self.path = path\n" \
                     "      self.name = os.path.basename(path)\n" \
                     "      self.extension = os.path.splitext(path)[1].replace('.', '').lower()\n"
        log_content = "2018-07-04 21:29:53 INFO - New request\n" \
                      "2018-07-04 21:30:35 INFO - New request\n" \
                      "2018-07-04 21:30:45 WARN - Invalid request\n"

        self.tearDown()

        os.mkdir(self.root_path)
        os.mkdir(self.sub1_path)
        os.mkdir(self.sub2_path)

        with open(self.txt_path, 'w') as fh:
            fh.write(txt_content)
        with open(self.py_path, 'w') as fh:
            fh.write(py_content)
        with open(self.log_path, 'w') as fh:
            fh.write(log_content)

    def tearDown(self):
        if os.path.exists(self.root_path):
            shutil.rmtree(self.root_path)

    def test__is_directory__valid_path__return_true(self):
        # Act
        result = DirWalker.is_directory(self.root_path)

        # Assert
        self.assertTrue(result)

    def test__is_directory__invalid_path__return_false(self):
        # Act
        result = DirWalker.is_directory(self.log_path)

        # Assert
        self.assertFalse(result)

    def test__is_directory__non_existing_directory__return_false(self):
        # Act
        result = DirWalker.is_directory(os.path.join(self.root_path, 'failure'))

        # Assert
        self.assertFalse(result)

    def test__constructor__default(self):
        # Act
        dw = DirWalker()

        # Assert
        self.assertIsNone(dw._allowed_extensions)
        self.assertTrue(dw._search_recursive)

    def test__constructor__presets(self):
        # Arrange
        ext = ['txt', 'py']

        # Act
        dw = DirWalker(ext, False)

        # Assert
        self.assertEqual(ext, dw._allowed_extensions)
        self.assertFalse(dw._search_recursive)

    def test__set_extension_filter__value_none__filter_none(self):
        # Arrange
        dw = DirWalker()

        # Act
        dw.set_allowed_extensions(None)

        # Assert
        self.assertIsNone(dw._allowed_extensions)

    def test__set_allowed_extensions__single_word__is_list(self):
        # Arrange
        dw = DirWalker()
        val = 'txt'

        # Act
        dw.set_allowed_extensions(val)

        # Assert
        self.assertEqual([val], dw._allowed_extensions)

    def test__set_allowed_extensions__multiple_words__is_list(self):
        # Arrange
        dw = DirWalker()
        val = ['txt', 'py']

        # Act
        dw.set_allowed_extensions(val)

        # Assert
        self.assertEqual(val, dw._allowed_extensions)

    def test__set_allowed_extensions__empty_list__set_none(self):
        # Arrange
        dw = DirWalker()
        val = []

        # Act
        dw.set_allowed_extensions(val)

        # Assert
        self.assertIsNone(dw._allowed_extensions)

    def test__set_search_recursive__none_boolean_value__set_true(self):
        # Arrange
        dw = DirWalker()
        val = 'wrong type'

        # Act
        dw.set_search_recursive(val)

        # Assert
        self.assertTrue(dw._search_recursive)

    def test__set_search_recursive__boolean_value__set_value(self):
        # Arrange
        dw = DirWalker()

        # Act
        dw.set_search_recursive(False)

        # Assert
        self.assertFalse(dw._search_recursive)

    def test__has_allowed_extension__filter_is_none__no_filtering(self):
        # Arrange
        dw = DirWalker(allowed_extensions=None)
        file = "MyFile.txt"

        # Act
        result = dw.has_allowed_extension(file)

        # Assert
        self.assertTrue(result)

    def test__has_allowed_extension__right_extension__include_file(self):
        # Arrange
        dw = DirWalker(allowed_extensions=['txt'])
        file = "MyFile.txt"

        # Act
        result = dw.has_allowed_extension(file)

        # Assert
        self.assertTrue(result)

    def test__has_allowed_extension__wrong_extension__exclude_file(self):
        # Arrange
        dw = DirWalker(allowed_extensions=['py'])
        file = "MyFile.txt"

        # Act
        result = dw.has_allowed_extension(file)

        # Assert
        self.assertFalse(result)

    def test__list_files__search_recursive__all_included(self):
        # Arrange
        dw = DirWalker()
        file_txt = File(self.txt_path)
        file_py = File(self.py_path)
        file_log = File(self.log_path)
        recursive_list = [file_txt, file_py, file_log]

        # Act
        result = dw.list_files(self.root_path)

        # Assert
        self.assertListEqual(sorted(recursive_list), sorted(result))

    def test__list_files_search__non_recursive__no_files_subdirectory(self):
        # Arrange
        dw = DirWalker(recursive=False)
        file_txt = File(self.txt_path)
        no_recursive_list = [file_txt, ]

        # Act
        result = dw.list_files(self.root_path)

        # Assert
        self.assertListEqual(sorted(no_recursive_list), sorted(result))

    def test__list_files__search_filter_extensions__include_files(self):
        # Arrange
        dw = DirWalker(allowed_extensions=['txt', '.log'])
        file_txt = File(self.txt_path)
        file_log = File(self.log_path)
        recursive_list = [file_txt, file_log]

        # Act
        result = dw.list_files(self.root_path)

        # Assert
        self.assertListEqual(sorted(recursive_list), sorted(result))

    def test__list_files__non_existing_directory__return_empty_list(self):
        # Act
        dw = DirWalker()
        result = dw.list_files(os.path.join(self.root_path, 'failure'))

        # Assert
        self.assertListEqual([], sorted(result))
