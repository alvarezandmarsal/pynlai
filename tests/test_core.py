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

    def test_sent_to_dep(self):
        s = u'I like green eggs and ham.'
        r = core.sent_to_dep(s, nlp)
        dep = [
            ['I', 'I', 'nsubj', 'like', 'VERB', 'like'],
            ['green eggs', 'eggs', 'dobj', 'like', 'VERB', 'like'],
            ['ham', 'ham', 'conj', 'eggs', 'NOUN', 'egg'],
        ]
        six.assertCountEqual(self, r, dep)

    def test_sent_to_pos(self):
        s = u'This is a test sentence.'
        r = core.sent_to_pos(s, nlp)
        pos = [
            ['This', 'this', 'DET'],
            ['is', 'be', 'VERB'],
            ['a', 'a', 'DET'],
            ['test', 'test', 'NOUN'],
            ['sentence', 'sentence', 'NOUN'],
            ['.', '.', 'PUNCT'],
        ]
        six.assertCountEqual(self, r, pos)

    def test_sent_to_sub(self):
        s = u'I like green eggs and ham,'
        r = core.sent_to_sub(s, nlp)
        sub = {
            ('I', '-PRON-', 'PRON'): [(1, 'like')],
        }
        six.assertCountEqual(self, r, sub)
