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


class TestParse(unittest.TestCase):

    nlp = en.load()

    def setUp(self):
        self.runner = CliRunner()

    def tearDown(self):
        pass

    def test_pipeline(self):
        s = u'This is a test sentence.'
        self.assertEqual(len(self.nlp(s)), 6)

    def test_sent_to_pos(self):
        s = u'This is a test sentence.'
        r = core.sent_to_pos(s, self.nlp)
        pos = [
            ('This', 'this', 'DET'),
            ('is', 'be', 'VERB'),
            ('a', 'a', 'DET'),
            ('test', 'test', 'NOUN'),
            ('sentence', 'sentence', 'NOUN'),
            ('.', '.', 'PUNCT'),
        ]
        six.assertCountEqual(self, r, pos)
