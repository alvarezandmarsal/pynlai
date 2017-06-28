# -*- coding: utf-8 -*-

'''
core
----


core functions and classes for pynlai.
'''


from operator import attrgetter
import six


_POS_FIELDS = (
    'text',
    'lemma',
    'lemma_',
    'pos',
    'pos_'
)

_DEP_FIELDS = (
    'text',
    'root.text',
    'root.dep',
    'root.dep_',
    'root.head.text',
    'root.head.lemma',
    'root.head.lemma_',
)


def sent_to_pos(sent, nlp, fs=None):
    '''
    returns lemma and parts-of-speech from spacy POS tagger
    requires pre-instantiated spacy nlp obj for performance
    see https://spacy.io/docs/usage/pos-tagging
    '''

    if type(sent) is not six.text_type:
        sent = six.u(sent)

    if not fs:
        fs = _POS_FIELDS

    doc = nlp(sent)

    return [[attrgetter(f)(w) for f in fs] for w in doc]


def sent_to_deps(sent, nlp, fs=None):
    '''
    returns noun chunks from spacy syntactic dependency parser
    requires pre-instantiated spacy nlp obj for performance
    see https://spacy.io/docs/usage/dependency-parse
    '''

    if type(sent) is not six.text_type:
        sent = six.u(sent)

    if not fs:
        fs = _DEP_FIELDS

    doc = nlp(sent)

    return [[attrgetter(f)(nc) for f in fs] for nc in doc.noun_chunks]
