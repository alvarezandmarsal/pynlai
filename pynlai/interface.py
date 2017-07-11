# -*- coding: utf-8 -*-

'''
interface
---------

collection for building natural language app interfaces
'''


from functools import wraps
from inspect import getmembers


class Trigger(object):
    '''
    base class for natural language triggers
    where call is an nl function and view is a dict from views
    output must match (key, value) tuples in criteria to trigger
    '''

    __pynlai_fcn = None

    def __init__(self, call, view, criteria):
        self.call = call
        self.view = view
        self.criteria = criteria


class Command(Trigger):
    '''
    class for triggering commands from natural language
    '''

    def __init__(self, call, view, criteria):
        super(Command, self).__init__(call, view, criteria)
        self.callback = lambda: self.__pynlai_fcn


class Argument(Trigger):
    '''
    class for triggering arguments from natural language
    where callback is called when triggered and returns a dict
    '''

    def __init__(self, call, view, criteria, callback):
        super(Argument, self).__init__(call, view, criteria)
        self.callback = callback


def nl_function(*triggers):
    '''
    decorator for registering a function in the pynlai
    '''

    def decorator(fcn):

        @wraps(fcn)
        def wrapper(*args, **kwargs):

            # associate function with triggers and vice versa
            fcn.__pynlai_triggers = triggers
            for t in triggers:
                t.__pynlai_fcn = fcn.__name__

            return fcn(*args, **kwargs)

        return wrapper

    return decorator


def run(doc, nlp):
    '''
    runs a natural language document through each registered object
    doc must either be a spacy Doc object or text
    '''

    args = dict()
    callbacks = list()
    command = lambda: None
    doc = nlp(doc) if type(doc) is not Doc else doc

    for fcn in getmembers(__name__):

        for t in getattr('__pynlai_triggers', ()):

            for s in doc.sents:

                # store callbacks on triggers meeting criteria
                o = create_view(t.call(doc=s, nlp=nlp), t.view)
                if all([c in o for c in t.criteria]):
                    callbacks.append((type(t.callback), t.callback))

    # handle stored callbacks
    for t, c in results:

        if t == Command:
            command = c

        elif t == Argument:
            args = dict(args.items() + c().items())

    return command(**args)
