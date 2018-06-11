#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
test_patterns
-------------

unit tests for pynlai patterns module
'''


from random import randint, shuffle
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
        nl = 'meet %s'
        chars = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        for i in range(0, 100):
            shuffle(chars)
            rnd = randint(4, 20)
            @patterns.verb('meet')
            def nl_function():
                return 'hello somebody'
            self.nl_function = nl_function
            r = pynlai.run(doc=nl % chars[:rnd], nlp=nlp, obj=self)
            self.assertDictEqual(r, {'nl_function': 'hello somebody'})

    def test_d_object(self):
        nl = 'meet julio on the street'
        @patterns.verb('meet')
        @patterns.d_object('meet', 'name', nlp)
        def nl_function(name):
            return name
        self.nl_function = nl_function
        r = pynlai.run(doc=nl, nlp=nlp, obj=self)
        self.assertDictEqual(r, {'nl_function': 'julio'})

    def test_p_object(self):
        nl = 'meet julio on the street'
        @patterns.verb('meet')
        @patterns.p_object('on', 'place', nlp, view_key='root.lemma_')
        def nl_function(place):
            return place
        self.nl_function = nl_function
        r = pynlai.run(doc=nl, nlp=nlp, obj=self)
        self.assertDictEqual(r, {'nl_function': 'street'})

    def test_regex(self):
        # slack ids known to cause nlp issues
        for u in ('U8C3B0NBX', 'U8BEWRQV7', 'U8CR0RKV4', 'U8CR3QZ7G'):
            for p in ('[A-Z0-9]{9}', '<@([A-Z0-9]{9})>'):
                nl = 'meet <@%s>' % u
                @patterns.verb('meet')
                @patterns.regex(p, 'name')
                def nl_function(name):
                    return name
                self.nl_function = nl_function
                r = pynlai.run(doc=nl, nlp=nlp, obj=self)
                self.assertDictEqual(r, {'nl_function': u})

    def test_command(self):
        nl = 'meet julio'
        @patterns.command('meet', 'name', nlp)
        def nl_function(name):
            return name
        self.nl_function = nl_function
        r = pynlai.run(doc=nl, nlp=nlp, obj=self)
        self.assertDictEqual(r, {'nl_function': 'julio'})
