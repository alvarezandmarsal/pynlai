# -*- coding: utf-8 -*-

'''
core
----

core functions and classes for pynlai.
'''


from operator import attrgetter
import six

import en_core_web_sm as en
from spacy.en import English
from spacy.tokens import Doc
from spacy.symbols import dobj, nsubj, VERB


_DEP_FIELDS = (
    'text',
    'root.text',
    'root.dep_',
    'root.head.text',
    'root.head.pos_',
    'root.head.lemma_',
)

_ENT_FIELDS = (
    'text',
    'label_',
)

_POS_FIELDS = (
    'text',
    'lemma_',
    'pos_'
)


def nlp_preprocess(nlp_model, flds_default):
    '''
    a decorator to pre-process kwargs passed to nlp functions
    provides optional nlp arg to all decorated functions
    '''

    def decorator(fcn):

        def wrapper(*args, **kwargs):

            name = fcn.__name__

            # validations
            if args:
                raise ValueError('pass args by name to %s' % name)

            if 'sent' not in kwargs and 'doc' not in kwargs:
                raise ValueError('pass either sent or doc to %s' % name)

            if 'doc' in kwargs and type(kwargs['doc']) is not Doc:
                raise ValueError('doc must be of type %s' % type(Doc))

            # pre-processors
            sent = kwargs.get('sent', bytes())
            if type(sent) is not six.text_type:
                kwargs['sent'] = six.u(sent)

            nlp = kwargs.get('nlp', None)
            if type(nlp) is not nlp_model:
                kwargs['nlp'] = en.load()

            doc = kwargs.get('doc', None)
            if type(doc) is not Doc:
                kwargs['doc'] = kwargs['nlp'](kwargs['sent'])
            else:
                kwargs['sent'] = kwargs['doc'].text

            kwargs.setdefault('flds', flds_default)

            # call decorated function with pre-processed kwargs
            return fcn(**kwargs)

        return wrapper

    return decorator


@nlp_preprocess(English, _DEP_FIELDS)
def find_dep(nlp, sent, doc, dep, pos, flds):
    '''
    finds dependencies in the sentence matching dep and (head) pos
    returns dict of deps: list(heads) where each is a tuple of fields
    '''

    res = dict()

    for w in doc:
        if w.dep == dep and w.head.pos == pos:
            d_fields = [attrgetter(f)(w) for f in flds]
            h_fields = [attrgetter(f)(w.head) for f in flds]
            heads = res.get(tuple(d_fields), [])
            heads.append(h_fields)

            res[tuple(d_fields)] = heads

    return res


@nlp_preprocess(English, _DEP_FIELDS)
def to_dep(nlp, sent, doc, flds):
    '''
    returns noun chunks from spacy syntactic dependency parser
    requires a sentence (sent) or an nlp document (doc)
    see https://spacy.io/docs/usage/dependency-parse
    '''

    return [[attrgetter(f)(nc) for f in flds] for nc in doc.noun_chunks]


@nlp_preprocess(English, _ENT_FIELDS)
def to_ent(nlp, sent, doc, flds):
    '''
    returns entities and annotations
    requires a sentence (sent) or an nlp document (doc)
    see https://spacy.io/docs/usage/entity-recognition
    '''

    return [[attrgetter(f)(e) for f in flds] for e in doc.ents]


@nlp_preprocess(English, _POS_FIELDS)
def to_obj(nlp, sent, doc, flds):
    '''
    finds the objects(s) of the sentence, which is the noun that is
    the recipient of a verb action
    requires a sentence (sent) or an nlp document (doc)
    '''

    return find_dep(dep=dobj, pos=VERB, **vars())


@nlp_preprocess(English, _POS_FIELDS)
def to_pos(nlp, sent, doc, flds):
    '''
    returns parts of speech from spacy POS tagger
    requires a sentence (sent) or an nlp document (doc)
    see https://spacy.io/docs/usage/pos-tagging
    '''

    return [[attrgetter(f)(w) for f in flds] for w in doc]


@nlp_preprocess(English, _POS_FIELDS)
def to_sub(nlp, sent, doc, flds):
    '''
    finds the subject(s) of the sentence, which is the noun that is
    performing the verb(s) in the sentence
    requires a sentence (sent) or an nlp document (doc)
    '''

    return find_dep(dep=nsubj, pos=VERB, **vars())
