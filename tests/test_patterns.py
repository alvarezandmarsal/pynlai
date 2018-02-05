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

    def test_command(self):
        nl = 'meet julio'
        @patterns.command('meet', 'name', nlp)
        def nl_function(name):
            return name
        self.nl_function = nl_function
        r = pynlai.run(doc=nl, nlp=nlp, obj=self)
        self.assertEqual(r, 'julio')
