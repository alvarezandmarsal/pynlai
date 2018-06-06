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


def verb(verb):
    '''
    a simple verb trigger pattern
    '''

    pos_fcn, pos_fields = func_view['pos']
    trigger = Trigger(
        pos_fcn,
        pos_fields,
        OrderedDict([
            ('lemma_', verb),
            ('pos_', 'VERB'),
        ]),
    )

    return nl_function(trigger)


def d_object(verb, key, nlp):
    '''
    a simple direct object of a verb argument pattern
    '''

    obj_fcn, obj_fields = func_view['obj']

    def _callback(sent):
        obj = obj_fcn(doc=sent, nlp=nlp).pop()
        view = create_view(obj, obj_fields)

        return dict([(key, view['orth_'])])

    trigger = Argument(
        obj_fcn,
        obj_fields,
        OrderedDict([
            ('dep_', 'dobj'),
            ('head.lemma_', verb),
        ]),
        _callback,
    )

    return nl_function(trigger)


def regex(pattern, key):
    '''
    a simple regex argument pattern
    '''

    def _callback(sent):
        r = re.search(pattern, sent)

        if r and r.groups():
            return dict([(key, r.groups()[-1])])

        elif r:
            return dict([(key, r.group(0))])

        return dict([(key, '')])

    # the callback is called exactly once
    trigger = Argument(
        lambda **kwargs: (1,),
        (),
        OrderedDict([]),
        _callback,
    )

    return nl_function(trigger)


def command(verb, target, nlp):
    '''
    a simple verb > target command phrase pattern
    ex:  meet julio
    '''

    pos_fcn, pos_fields = func_view['pos']
    obj_fcn, obj_fields = func_view['obj']

    def _callback(sent):
        obj_fcn, obj_fields = func_view['obj']
        obj = obj_fcn(doc=sent, nlp=nlp).pop()
        view = create_view(obj, obj_fields)

        return dict([(target, view['orth_'])])

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
