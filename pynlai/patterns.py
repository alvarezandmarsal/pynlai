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

    # pos pipeline is more encompassing
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


def _object(word, pos, dep, view_key, key, nlp):
    '''
    an object meta pattern
    ex: "meet julio" word=meet, pos=VERB, dep=dobj view_key=text > julio
    '''

    # nc pipeline gives better NLP, use regex for encoded objs
    nc_fcn, nc_fields = func_view['nc']

    def _callback(sent):
        nc = nc_fcn(doc=sent, nlp=nlp).pop()
        view = create_view(nc, nc_fields)

        return dict([(key, view[view_key])])

    trigger = Argument(
        nc_fcn,
        nc_fields,
        OrderedDict([
            ('root.dep_', dep),
            ('root.head.lemma_', word),
            ('root.head.pos_', pos),
        ]),
        _callback,
    )

    return nl_function(trigger)


def d_object(verb, key, nlp, view_key='text'):
    '''
    a simple direct object of a verb argument pattern
    ex: "meet julio" returns julio
    '''

    return _object(verb, 'VERB', 'dobj', view_key, key, nlp)


def p_object(prep, key, nlp, view_key='text'):
    '''
    a simple object of a preposition argument pattern
    ex: "on file" returns file
    '''

    return _object(prep, 'ADP', 'pobj', view_key, key, nlp)


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
    a simple verb > target command phrase pattern (legacy)
    ex:  meet julio
    note:  better to compose with verb, d_object, etc.
    '''

    pos_fcn, pos_fields = func_view['pos']
    nc_fcn, nc_fields = func_view['nc']

    def _callback(sent):
        nc = nc_fcn(doc=sent, nlp=nlp).pop()
        view = create_view(nc, nc_fields)

        return dict([(target, view['text'])])

    trigger = Trigger(
        pos_fcn,
        pos_fields,
        OrderedDict([
            ('lemma_', verb),
            ('pos_', 'VERB'),
        ]),
    )

    argument = Argument(
        nc_fcn,
        nc_fields,
        OrderedDict([
            ('root.dep_', 'dobj'),
            ('root.head.lemma_', verb),
            ('root.head.pos_', 'VERB'),
        ]),
        _callback,
    )

    return nl_function(trigger, argument)
