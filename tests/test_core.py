#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
test_core
---------

unit tests for pynlai package core functionality
'''


import six
import unittest

from click.testing import CliRunner
import en_core_web_sm as en

from pynlai import core
from pynlai import cli


nlp = en.load()


class TestCore(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def tearDown(self):
        pass

    def test_nlp(self):
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

    def test_sent_to_deps(self):
        s = u'I like green eggs and ham.'
        r = core.sent_to_deps(s, nlp)
        deps = [
            ['I', 'I', 425, 'nsubj', 'like', 570, 'like'],
            ['green eggs', 'eggs', 412, 'dobj', 'like', 570, 'like'],
            ['ham', 'ham', 406, 'conj', 'eggs', 5480, 'egg'],
        ]
        six.assertCountEqual(self, r, deps)
