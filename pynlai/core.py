# -*- coding: utf-8 -*-

'''
core
----


core functions and classes for pynlai.
'''


import six

import en_core_web_sm as en


def sent_to_pos(sent, nlp=None):
    '''
    returns lemma and Google Universal POS tags for each word in sent
    see https://spacy.io/docs/usage/pos-tagging
    '''

    sent = six.u(sent) if type(sent) is not six.text_type else sent
    nlp = en.load() if not nlp else nlp

    return [(w.text, w.lemma_, w.pos_) for w in nlp(sent)]
