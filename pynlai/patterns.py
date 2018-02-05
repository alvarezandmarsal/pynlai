# -*- coding: utf-8 -*-

'''
patterns
--------

a collection of common nlp patterns
'''


from collections import OrderedDict

from .cli import func_view
from .core import create_view
from .interface import (Trigger, Argument, nl_function)


def command(verb, target, nlp):
    '''
    a simple verb > target command phrase
    ex:  meet julio
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

    def _callback(sent):
        obj = obj_fcn(doc=sent, nlp=nlp).pop()
        view = create_view(obj, obj_fields)

        return dict([(target, view['orth_'])])

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
