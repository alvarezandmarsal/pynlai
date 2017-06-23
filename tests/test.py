#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
test
----

core unit tests for pynlai package
'''


import unittest
from click.testing import CliRunner

from pynlai import pynlai
from pynlai import cli


class Test(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def tearDown(self):
        pass

    def test_command_line_interface(self):
        result = self.runner.invoke(
            cli.main,
            catch_exceptions=False,
        )
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(
            cli.main,
            ['--help'],
            catch_exceptions=False,
        )
        self.assertEqual(result.exit_code, 0)
        self.assertTrue('Show this message and exit' in result.output)
