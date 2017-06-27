# -*- coding: utf-8 -*-

'''
core
----


core functions and classes for pynlai.
'''


from operator import attrgetter
import six


def sent_to_pos(sent, nlp, pos=None):
    '''
    returns lemma and parts-of-speech from spacy POS tagger
    requires pre-instantiated spacy nlp obj for performance
    see https://spacy.io/docs/usage/pos-tagging
    '''

    if type(sent) is not six.text_type:
        sent = six.u(sent)

    if not pos:
        pos = ('text', 'lemma', 'lemma_', 'pos', 'pos_')

    doc = nlp(sent)

    return [[attrgetter(p)(w) for p in pos] for w in doc]


def sent_to_deps(sent, nlp, deps=None):
    '''
    returns noun chunks from spacy syntactic dependency parser
    requires pre-instantiated spacy nlp obj for performance
    see https://spacy.io/docs/usage/dependency-parse
    '''

    if type(sent) is not six.text_type:
        sent = six.u(sent)

    if not deps:
        deps = ('text', 'root.text', 'root.dep_', 'root.head.text')

    doc = nlp(sent)

    return [[attrgetter(d)(nc) for d in deps] for nc in doc.noun_chunks]
