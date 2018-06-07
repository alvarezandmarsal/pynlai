# -*- coding: utf-8 -*-

'''
interface
---------

collection for building natural language app interfaces
'''


from functools import wraps
from inspect import getmembers

from spacy.lang.en import English

from pynlai import core


class Trigger(object):
    '''
    natural language trigger where:
      call is a nl fcn from core that returns a list of spacy objects
      view is a list of keys to be used with core.create_view
      criteria is a list of (key, value) tuples to match in view
      callback is automatically set to decorated function by run
    '''

    def __init__(self, call, view, criteria, callback=None):
        self.call = call
        self.view = view
        self.criteria = criteria
        self.callback = callback


class Argument(Trigger):
    '''
    natural language trigger that is an argument to a decorated function
    where callback is a fcn to process view results and return a dict
    '''

    argument = True

    def __init__(self, call, view, criteria, callback):
        super(Argument, self).__init__(call, view, criteria, callback)


def nl_function(*triggers):
    '''
    decorator for registering a function in the pynlai
    '''

    def decorator(fcn):

        # inject triggers into decorated function
        pt = getattr(fcn, '__pynlai_triggers', ())
        setattr(fcn, '__pynlai_triggers', pt + triggers)

        @wraps(fcn)
        def wrapper(*args, **kwargs):

            return fcn(*args, **kwargs)

        return wrapper

    return decorator


@core.nlp_preprocess(English)
def run(doc, nlp, obj):
    '''
    runs a natural language document through each registered object
    and returns a dict of results by member object name
    '''

    callbacks = dict()
    result = dict()

    # process all pynlai triggers contained in module functions
    for name, fcn in getmembers(obj):

        if not hasattr(fcn, '__pynlai_triggers'):
            continue

        callbacks[name] = list()

        # store all triggers meeting criteria
        for t in getattr(fcn, '__pynlai_triggers'):

            for s in doc.sents:

                for e in t.call(doc=s.text, nlp=nlp):

                    nl_view = core.create_view(e, t.view)

                    if set(t.criteria.items()) <= set(nl_view.items()):
                        callback = t.callback or fcn
                        callbacks[name].append((t, s.text, callback))

    # handle stored triggers localized by function
    for name in callbacks.keys():

        if not callbacks[name]:
            continue

        args = dict()
        def command(*args, **kwargs): return None  # noqa

        for trigger, sentence, callback in callbacks[name]:

            if hasattr(trigger, 'argument'):
                args.update(callback(sentence))

            else:
                command = callback  # noqa

        result[name] = command(**args)

    return result
