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
    '''

    pass


class Command(Trigger):
    '''
    class for triggering commands from natural language
    '''

    pass


class Argument(Trigger):
    '''
    class for triggering arguments from natural language
    '''

    pass


def nl_function(*triggers):
    '''
    decorator for registering a function in the pynlai
    '''

    def decorator(fcn):

        @wraps(fcn)
        def wrapper(*args, **kwargs):

            fcn.__pynlai_triggers = triggers

            return fcn(*args, **kwargs)

        return wrapper

    return decorator


def run(sents):
    '''
    runs a document through each registered object
    '''

    for fcn in getmembers(__name__):

        for t in getattr('__pynlai_triggers', ()):

            pass
