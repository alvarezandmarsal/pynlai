#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
test_patterns
-------------

unit tests for pynlai patterns module
'''


import six
import unittest

import en_core_web_sm as en

import pynlai
from pynlai import patterns

from .shared import *


class TestPatterns(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_verb(self):
        nl = 'meet julio'
        @patterns.verb('meet')
        def nl_function():
            return 'it works!'
        self.nl_function = nl_function
        r = pynlai.run(doc=nl, nlp=nlp, obj=self)
        self.assertEqual(r, 'it works!')

    def test_d_object(self):
        nl = 'meet julio'
        @patterns.verb('meet')
        @patterns.d_object('meet', 'name', nlp)
        def nl_function(name):
            return name
        self.nl_function = nl_function
        r = pynlai.run(doc=nl, nlp=nlp, obj=self)
        self.assertEqual(r, 'julio')

    def test_regex(self):
        nl = 'meet <@U8BEWRQV7>'
        @patterns.verb('meet')
        @patterns.regex('<@[A-Z0-9]{9}>', 'name')
        def nl_function(name):
            return name
        self.nl_function = nl_function
        r = pynlai.run(doc=nl, nlp=nlp, obj=self)
        self.assertEqual(r, '<@U8BEWRQV7>')
        nl = 'meet <@U8CR3QZ7G>'
        @patterns.verb('meet')
        @patterns.regex('<@([A-Z0-9]{9})>', 'name')
        def nl_function(name):
            return name
        self.nl_function = nl_function
        r = pynlai.run(doc=nl, nlp=nlp, obj=self)
        self.assertEqual(r, 'U8CR3QZ7G')

    def test_command(self):
        nl = 'meet julio'
        @patterns.command('meet', 'name', nlp)
        def nl_function(name):
            return name
        self.nl_function = nl_function
        r = pynlai.run(doc=nl, nlp=nlp, obj=self)
        self.assertEqual(r, 'julio')
