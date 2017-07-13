# -*- coding: utf-8 -*-

'''
interface
---------

collection for building natural language app interfaces
'''


from functools import wraps
from inspect import getmembers

from spacy.en import English

from pynlai import core


class Trigger(object):
    '''
    natural language trigger where call is nl fcn, view is key list,
    and criteria is a list of tuples to match in view to trigger;
    callback is set to decorated function by run
    '''

    def __init__(self, call, view, criteria, callback=None):
        self.call = call
        self.view = view
        self.criteria = criteria
        self.callback = callback


class Argument(Trigger):
    '''
    natural language trigger that is an argument to a decorated function
    where callback is a function to process nl_view and return a dict
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
        setattr(fcn, '__pynlai_triggers', triggers)

        @wraps(fcn)
        def wrapper(*args, **kwargs):

            return fcn(*args, **kwargs)

        return wrapper

    return decorator


@core.nlp_preprocess(English)
def run(doc, nlp, obj):
    '''
    runs a natural language document through each registered object
    '''

    args = dict()
    callbacks = list()
    def command(*args, **kwargs): return None  # noqa

    # store callback for triggers meeting criteria
    for _, fcn in getmembers(obj):

        for trigger in getattr(fcn, '__pynlai_triggers', ()):

            for sent in doc.sents:

                for e in trigger.call(doc=sent.text, nlp=nlp):

                    nl_view = core.create_view(e, trigger.view)

                    if nl_view == trigger.criteria:
                        callback = trigger.callback or fcn
                        callbacks.append((trigger, nl_view, callback))

    # handle stored callbacks
    for trigger, nl_view, callback in callbacks:

        if hasattr(trigger, 'argument'):
            args.update(trigger.callback(nl_view))

        else:
            command = callback  # noqa

    return command(**args)
