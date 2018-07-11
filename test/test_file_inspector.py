#! /usr/bin/env python
# -*- coding: utf-8 -*-
from src.file_inspector import FileInspector
import tempfile
import unittest
import shutil
import os


__author__ = 'Stephan Tischer'
__date__ = '2018-07-10'
__version__ = '0.1.0'


class TestFileInspector(unittest.TestCase):
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

        self.txt_content = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr,\n" \
                           "sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,\n" \
                           "sed diam voluptua."
        self.py_content = "#! /usr/bin/env python\n" \
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
        self.log_content = "2018-07-04 21:29:53 INFO - New request\n" \
                           "2018-07-04 21:30:35 INFO - New request\n" \
                           "2018-07-04 21:30:45 WARN - Invalid request\n"

        self.tearDown()

        os.mkdir(self.root_path)
        os.mkdir(self.sub1_path)
        os.mkdir(self.sub2_path)

        with open(self.txt_path, 'w') as fh:
            fh.write(self.txt_content)
        with open(self.py_path, 'w') as fh:
            fh.write(self.py_content)
        with open(self.log_path, 'w') as fh:
            fh.write(self.log_content)

    def tearDown(self):
        if os.path.exists(self.root_path):
            shutil.rmtree(self.root_path)

    def test__read_file__existing_file__read_all(self):
        # Act
        result = FileInspector.read_file(self.txt_path)

        # Assert
        self.assertEqual(self.txt_content, result)

    def test__read_file__non_existing_file__return_empty(self):
        # Act
        result = FileInspector.read_file(os.path.join(self.sub1_path, 'no-file.txt'))

        # Assert
        self.assertEqual("", result)

    def test__read_file__path_to_directory__return_empty(self):
        # Act
        result = FileInspector.read_file(os.path.join(self.sub1_path))

        # Assert
        self.assertEqual("", result)

    def test__get_numbers_of_lines__one_line(self):
        # Arrange
        content = "This is just one line"

        # Act
        result = FileInspector.get_numbers_of_lines(content)

        # Assert
        self.assertEqual(1, result)

    def test__get_numbers_of_lines__multiple_lines(self):
        # Arrange
        content = "This is the first line\n" \
                  "This is the second line\n" \
                  "and a third one"

        # Act
        result = FileInspector.get_numbers_of_lines(content)

        # Assert
        self.assertEqual(3, result)

    def test__get_numbers_of_lines__using_offset(self):
        # Arrange
        content = "This is the first line\n" \
                  "This is the second line\n" \
                  "and a third one"

        # Act
        result = FileInspector.get_numbers_of_lines(content, 4)

        # Assert
        self.assertEqual(3 + 4, result)

    def test__split_content__in_middle(self):
        # Arrange
        content = "This is just one line"

        # Act
        result_first, result_second = FileInspector.split_content(content, content.find("just"))

        # Assert
        self.assertEqual("This is ", result_first)
        self.assertEqual("just one line", result_second)

    def test__split_content__at_beginning(self):
        # Arrange
        content = "This is just one line"

        # Act
        result_first, result_second = FileInspector.split_content(content, 0)

        # Assert
        self.assertEqual("", result_first)
        self.assertEqual("This is just one line", result_second)

    def test__split_content__at_end(self):
        # Arrange
        content = "This is just one line"

        # Act
        result_first, result_second = FileInspector.split_content(content, len(content))

        # Assert
        self.assertEqual("This is just one line", result_first)
        self.assertEqual("", result_second)

    def test__split_content__pos_minus_one(self):
        # Arrange
        content = "This is just one line"

        # Act
        result_first, result_second = FileInspector.split_content(content, -1)

        # Assert
        self.assertEqual("This is just one line", result_first)
        self.assertEqual("", result_second)

    def test__exec_simple_search__term_in_file__return_file(self):
        # Arrange
        path = self.txt_path
        content = self.txt_content
        term = "sed"

        # Act
        result = FileInspector.exec_simple_search(path, content, term)

        # Assert
        self.assertEqual(list, type(result))
        self.assertEqual(1, len(result))
        self.assertEqual(path, result[0].file)
        self.assertEqual(term, result[0].term)
        self.assertIsNone(result[0].line_number)

    def test__exec_simple_search__term_not_in_file__return_empty(self):
        # Arrange
        path = self.txt_path
        content = self.txt_content
        term = "not-found"

        # Act
        result = FileInspector.exec_simple_search(path, content, term)

        # Assert
        self.assertEqual(list, type(result))
        self.assertEqual(0, len(result))

    def test__exec_simple_search__term_has_line_break__return_file(self):
        # Arrange
        path = self.txt_path
        content = self.txt_content
        term = "elitr,\nsed"

        # Act
        result = FileInspector.exec_simple_search(path, content, term)

        # Assert
        self.assertEqual(list, type(result))
        self.assertEqual(1, len(result))

    def test__exec_search_show_lines__term_in_file__return_file(self):
        # Arrange
        path = self.txt_path
        content = self.txt_content
        term = "sed"

        # Act
        result = FileInspector.exec_search_show_lines(path, content, term)

        # Assert
        self.assertEqual(list, type(result))
        self.assertEqual(2, len(result))
        self.assertEqual(path, result[0].file)
        self.assertEqual(term, result[0].term)
        self.assertEqual(2, result[0].line_number)
        self.assertEqual(path, result[1].file)
        self.assertEqual(term, result[1].term)
        self.assertEqual(3, result[1].line_number)

    def test__exec_search_show_lines__single_line__return_file(self):
        # Arrange
        path = self.txt_path
        content = "This is just one line"
        term = "just"

        # Act
        result = FileInspector.exec_search_show_lines(path, content, term)

        # Assert
        self.assertEqual(list, type(result))
        self.assertEqual(1, len(result))
        self.assertEqual(path, result[0].file)
        self.assertEqual(term, result[0].term)
        self.assertEqual(1, result[0].line_number)

    def test__exec_search_show_lines__term_not_in_file__return_empty(self):
        # Arrange
        path = self.txt_path
        content = self.txt_content
        term = "not-found"

        # Act
        result = FileInspector.exec_search_show_lines(path, content, term)

        # Assert
        self.assertEqual(list, type(result))
        self.assertEqual(0, len(result))

    def test__exec_search_show_lines__term_has_line_break__return_file(self):
        # Arrange
        path = self.txt_path
        content = self.txt_content
        term = "elitr,\nsed"

        # Act
        result = FileInspector.exec_search_show_lines(path, content, term)

        # Assert
        self.assertEqual(list, type(result))
        self.assertEqual(1, len(result))
        self.assertEqual(path, result[0].file)
        self.assertEqual(term, result[0].term)
        self.assertEqual(1, result[0].line_number)

    def test__exec_search_show_lines__term_has_line_break__multiple_hits__return_files(self):
        # Arrange
        path = self.py_path
        content = self.py_content
        term = "str\n  "

        # Act
        result = FileInspector.exec_search_show_lines(path, content, term)

        # Assert
        self.assertEqual(list, type(result))
        self.assertEqual(2, len(result))
        self.assertEqual(path, result[0].file)
        self.assertEqual(term, result[0].term)
        self.assertEqual(14, result[0].line_number)
        self.assertEqual(path, result[1].file)
        self.assertEqual(term, result[1].term)
        self.assertEqual(15, result[1].line_number)

    def test__search_worker__simple_search__return_one_term(self):
        # Arrange
        path = self.txt_path
        terms = "sed"

        # Act
        result = FileInspector.search_worker(path, terms, False, False)

        # Assert
        self.assertEqual(list, type(result))
        self.assertEqual(1, len(result))

    def test__search_worker__simple_search__return_multiple_terms(self):
        # Arrange
        path = self.txt_path
        terms = ["sed", "Lorem"]

        # Act
        result = FileInspector.search_worker(path, terms, False, False)

        # Assert
        self.assertEqual(list, type(result))
        self.assertEqual(2, len(result))

    def test__search_worker__simple_search__multiple_terms_case_sensitive(self):
        # Arrange
        path = self.txt_path
        terms = ["sed", "lorem"]

        # Act
        result = FileInspector.search_worker(path, terms, True, False)

        # Assert
        self.assertEqual(list, type(result))
        self.assertEqual(1, len(result))

    def test__search_worker__search_show_lines__return_one_term(self):
        # Arrange
        path = self.txt_path
        terms = "sed"

        # Act
        result = FileInspector.search_worker(path, terms, False, True)

        # Assert
        self.assertEqual(list, type(result))
        self.assertEqual(2, len(result))

    def test__search_worker__search_show_lines__multiple_terms(self):
        # Arrange
        path = self.txt_path
        terms = ["sed", "Lorem"]

        # Act
        result = FileInspector.search_worker(path, terms, False, True)

        # Assert
        self.assertEqual(list, type(result))
        self.assertEqual(3, len(result))

    def test__search_worker__search_show_lines__multiple_terms_case_sensitive(self):
        # Arrange
        path = self.txt_path
        terms = ["sed", "lorem"]

        # Act
        result = FileInspector.search_worker(path, terms, True, True)

        # Assert
        self.assertEqual(list, type(result))
        self.assertEqual(2, len(result))

    def test__inspect_files__multiple_files__simple_search(self):
        # Arrange
        paths = [self.txt_path, self.py_path, self.log_path]
        terms = ["2018"]

        # Act
        result = FileInspector.inspect_files(paths, terms, False, False)

        # Assert
        self.assertEqual(list, type(result))
        self.assertEqual(2, len(result))

    def test__inspect_files__multiple_files__search_show_lines(self):
        # Arrange
        paths = [self.txt_path, self.py_path, self.log_path]
        terms = ["2018"]

        # Act
        result = FileInspector.inspect_files(paths, terms, False, True)

        # Assert
        self.assertEqual(list, type(result))
        self.assertEqual(4, len(result))
