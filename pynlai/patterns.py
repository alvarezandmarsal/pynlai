# -*- coding: utf-8 -*-

'''
patterns
--------

a collection of common nlp patterns
'''


from collections import OrderedDict
import re

from .cli import func_view
from .core import create_view
from .interface import (Trigger, Argument, nl_function)


def _command(verb, target, _callback):
    '''
    a command phrase meta pattern
    '''

    pos_fcn, pos_fields = func_view['pos']
    obj_fcn, obj_fields = func_view['obj']

    trigger = Trigger(
        pos_fcn,
        pos_fields,
        OrderedDict([
            ('lemma_', verb),
            ('pos_', 'VERB'),
        ]),
    )

    argument = Argument(
        obj_fcn,
        obj_fields,
        OrderedDict([
            ('dep_', 'dobj'),
            ('head.lemma_', verb),
        ]),
        _callback,
    )

    return nl_function(trigger, argument)


def command(verb, target, nlp):
    '''
    a simple verb > target command phrase pattern
    ex:  meet julio
    '''

    def _callback(sent):
        obj_fcn, obj_fields = func_view['obj']
        obj = obj_fcn(doc=sent, nlp=nlp).pop()
        view = create_view(obj, obj_fields)

        return dict([(target, view['orth_'])])

    return _command(verb, target, _callback)


def command_regex(verb, target, pattern):
    '''
    a simple verb > target command phrase pattern
    with regex target pattern matching
    '''

    def _callback(sent):
        r = re.search(pattern, sent)

        if r:
            return dict([(target, r.group(0))])

        return dict([(target, '')])

    return _command(verb, target, _callback)
