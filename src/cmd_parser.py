#! /usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os


__author__ = 'Stephan Tischer'
__date__ = '2018-07-09'
__version__ = '0.1.0'


class CmdParser:
    """
    All tools to parse the commandline parameter
    """

    @staticmethod
    def parse(args):
        """ Parse the given commandline parameter

        :param args: Commandline parameter
        :return: Parsed result
        """

        parser = argparse.ArgumentParser(
            description="Search the content of all files in the given directory for the occurrences of a string"
        )

        parser.add_argument(
            dest="search",
            help="Search for (separate multiple terms by space)",
            metavar="Term",
            type=str,
            nargs="+"
        )
        parser.add_argument(
            "-d", "--dir", dest="dir",
            help="Path to directory which should be searched",
            metavar="Path",
            type=str,
            default=os.getcwd()
        )
        parser.add_argument(
            "-e", "--extensions", dest="extensions",
            help="Only look into files with the given extensions (separate multiple extensions by space)",
            metavar="Extension",
            type=str,
            nargs='*',
            default=None
        )
        parser.add_argument(
            "-l", "--lines", dest="lines",
            help="Show number of line in which term was found",
            action="store_true"
        )
        parser.add_argument(
            "-cs", "--case-sensitive", dest="case_sensitive",
            help="Execute search case sensitive",
            action="store_true"
        )
        parser.add_argument(
            "--long", dest="long",
            help="Show complete path to file",
            action="store_true"
        )
        parser.add_argument(
            "-ns", "--no-subdirectories", dest="recursive",
            help="Exclude subdirectories from the search",
            action="store_false"
        )

        cmd = parser.parse_args(args)

        if cmd.extensions is not None:
            for i in range(len(cmd.extensions)):
                cmd.extensions[i] = cmd.extensions[i].replace('.', '').lower()

        return cmd
