#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
test_parse
----------

unit tests for pynlai package parsing functionality
'''


import six
import unittest

from click.testing import CliRunner
import en_core_web_sm as en

from pynlai import core
from pynlai import cli


nlp = en.load()


class TestParse(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def tearDown(self):
        pass

    def test_pipeline(self):
        s = u'This is a test sentence.'
        self.assertEqual(len(nlp(s)), 6)

    def test_sent_to_pos(self):
        s = u'This is a test sentence.'
        r = core.sent_to_pos(s, nlp)
        pos = [
            ['This', 552, 'this', 88, 'DET'],
            ['is', 536, 'be', 98, 'VERB'],
            ['a', 506, 'a', 88, 'DET'],
            ['test', 1877, 'test', 90, 'NOUN'],
            ['sentence', 2499, 'sentence', 90, 'NOUN'],
            ['.', 453, '.', 95, 'PUNCT'],
        ]
        six.assertCountEqual(self, r, pos)
