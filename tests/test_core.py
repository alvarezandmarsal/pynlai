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
from spacy.tokens import Doc

from pynlai import core
from pynlai import cli


nlp = en.load()


class TestCore(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def tearDown(self):
        pass

    def test_nlp_preprocess(self):
        try:
            core.to_dep('Test.', nlp)
        except ValueError as e:
            self.assertTrue('pass args by name' in str(e))
        try:
            core.to_dep(nlp=nlp)
        except ValueError as e:
            self.assertTrue('pass either sent or doc' in str(e))
        try:
            core.to_dep(doc='Test.')
        except ValueError as e:
            self.assertTrue('doc must be of type' in str(e))
        r = core.to_dep(doc=Doc(nlp.vocab))
        six.assertCountEqual(self, r, [])

    def test_to_dep(self):
        s = 'I like green eggs and ham.'
        r = core.to_dep(sent=s, nlp=nlp)
        dep = [
            ['I', 'I', 'nsubj', 'like', 'VERB', 'like'],
            ['green eggs', 'eggs', 'dobj', 'like', 'VERB', 'like'],
            ['ham', 'ham', 'conj', 'eggs', 'NOUN', 'egg'],
        ]
        six.assertCountEqual(self, r, dep)

    def test_to_ent(self):
        s = 'London is a big city in the United Kingdom.'
        r = core.to_ent(sent=s, nlp=nlp)
        ent = [
            ['London', 'GPE'],
            ['the United Kingdom', 'GPE'],
        ]
        six.assertCountEqual(self, r, ent)

    def test_to_obj(self):
        s = 'I like green eggs and ham,'
        r = core.to_obj(sent=s, nlp=nlp)
        sub = {
            ('eggs', 'egg', 'NOUN'): [('like', 'like', 'VERB')],
        }
        six.assertCountEqual(self, r, sub)

    def test_to_pos(self):
        s = 'This is a test sentence.'
        r = core.to_pos(sent=s, nlp=nlp)
        pos = [
            ['This', 'this', 'DET'],
            ['is', 'be', 'VERB'],
            ['a', 'a', 'DET'],
            ['test', 'test', 'NOUN'],
            ['sentence', 'sentence', 'NOUN'],
            ['.', '.', 'PUNCT'],
        ]
        six.assertCountEqual(self, r, pos)

    def test_to_sub(self):
        s = 'I like green eggs and ham,'
        r = core.to_sub(sent=s, nlp=nlp)
        sub = {
            ('I', '-PRON-', 'PRON'): [('like', 'like', 'VERB')],
        }
        six.assertCountEqual(self, r, sub)
