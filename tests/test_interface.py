#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
test_interface
--------------

unit tests for pynlai interface module
'''


import six
import unittest

import pynlai
from pynlai import core
from pynlai import views


class TestCore(unittest.TestCase):

    def setUp(self):
        @pynlai.nl_function(
            pynlai.Trigger(
                core.to_pos,
                views._POS_TOKEN['HR'],
                [
                    ('orth_', 'Test'),
                    ('pos_', 'NOUN'),
                ],
            ),
        )
        def nl_test():
            return True
        self.nl_test = nl_test

    def tearDown(self):
        pass

    def test_nl_function(self):
        a_1 = '__pynlai_triggers'
        a_2 = '__pynlai_fcn'
        self.assertTrue(hasattr(self.nl_test, a_1))
        self.assertTrue(hasattr(getattr(self.nl_test, a_1)[0], a_2))

    def test_run(self):
        pass
