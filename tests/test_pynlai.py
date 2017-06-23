#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
test
----

unit tests for pynlai package
'''



import unittest
from click.testing import CliRunner

from pynlai import pynlai
from pynlai import cli


class TestPynlai(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def tearDown(self):
        pass

    def test_000_something(self):
        self.assertTrue(True)

    def test_command_line_interface(self):
        result = self.runner.invoke(cli.main)
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(cli.main, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue('--help  Show this message' in result.output)
