# -*- coding: utf-8 -*-

'''
core
----


core functions and classes for pynlai.
'''


import six


def sent_to_pos(sent, nlp, pos=None):
    '''
    returns lemma and POS for each word in sentence
    requires pre-instantiated spacy nlp obj for performance
    see https://spacy.io/docs/usage/pos-tagging
    '''

    sent = six.u(sent) if type(sent) is not six.text_type else sent
    pos = ('text', 'lemma', 'lemma_', 'pos', 'pos_') if not pos else pos

    return [[getattr(w, p) for p in pos] for w in nlp(sent)]
