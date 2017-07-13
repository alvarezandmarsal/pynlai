#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
test_interface
--------------

unit tests for pynlai interface module
'''


from collections import OrderedDict
import six
import unittest

import en_core_web_sm as en

import pynlai
from pynlai import core
from pynlai import views

from .shared import *


class TestInterface(unittest.TestCase):

    def setUp(self):
        self.nl = 'Test the nl_function with a set to 1.'
        self.trigger = pynlai.Trigger(
            core.to_obj,
            views._DEP_TOKEN['HR'],
            OrderedDict([
                ('orth_', 'nl_function'),
                ('lemma_', 'nl_function'),
                ('dep_', 'dobj'),
                ('head.orth_', 'Test'),
                ('head.lemma_', 'test'),
                ('head.pos_', 'VERB'),
            ]),
        )
        def arg_callback(*args, **kwargs): return {'a': True}
        self.argument = pynlai.Argument(
            core.to_obj,
            views._DEP_TOKEN['HR'],
            OrderedDict([
                ('orth_', 'nl_function'),
                ('lemma_', 'nl_function'),
                ('dep_', 'dobj'),
                ('head.orth_', 'Test'),
                ('head.lemma_', 'test'),
                ('head.pos_', 'VERB'),
            ]),
            arg_callback,
        )
        @pynlai.nl_function(
            self.trigger,
            self.argument,
        )
        def nl_function(a):
            return a
        self.nl_function = nl_function

    def tearDown(self):
        pass

    def test_decorator(self):
        self.assertTrue(hasattr(self.nl_function, '__pynlai_triggers'))

    def test_run(self):
        self.assertTrue(pynlai.run(doc=self.nl, nlp=nlp, obj=self))
