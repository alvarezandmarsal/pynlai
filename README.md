# pynlai

[![pypi](https://img.shields.io/pypi/v/pynlai.svg)](
https://pypi.python.org/pypi/pynlai)
[![tci](https://img.shields.io/travis/alvarezandmarsal/pynlai.svg)](
https://travis-ci.org/alvarezandmarsal/pynlai)
[![rtd](https://readthedocs.org/projects/pynlai/badge/?version=latest)](
https://pynlai.readthedocs.io/en/latest/?badge=latest)

PYthon Natural Language Application Interface library.

* Free software: MIT license
* Documentation: https://pynlai.readthedocs.io.

## Why pynlai?

pynlai was created to provide a way for non-technical users to interact
with backend applications using natural language.  Developers can simply
write an app and use pynlai to process text commands from any source
(e.g. irc, slack, email, etc.) by decorating their functions with
natural language triggers.

## Getting started

To get started with pynlai, you first need to have an idea of the types
of command sentences you expect from your users and how those sentences
will be parsed by spaCy.

For example, let's say you have the following function in your app:

```python
def nl_function(value):
```

And you expect a user might say:

```
Test the nl_function with value set to 1.
```

The first step is to use pynlai's cli to test how spaCy will parse that
sentence.

Clone the pynlai repo and build the docker dev containers
(Note: you must have docker and docker-compose installed, see
[installation instructions](https://docs.docker.com/compose/install/)):


```shell
$ docker-compose docker-compose-dev.yml build
```

Parse sentences with the `parse` cli command:

```shell
$ docker-compose -f docker-compose-dev.yml run --rm pynlai \
      pynlai parse "This is a test sentence."
```

Try to parse the sentence using the entire pynlai nl pipeline.  To see a
list of available options, use:

```shell
$ docker-compose docker-compose-dev.yml run --rm pynlai pynlai --help
```

Look for a pipeline function that isolates the command, usually the
dependency object parser `--pipeline obj` which gives us the following
for our test sentence:

```shell
$ docker-compose -f docker-compose-dev.yml run --rm pynlai \
      pynlai --pipeline obj \
      parse "Test the nl_function with value set to 1."
('to_obj',
 [OrderedDict([
     ('orth_', 'nl_function'),
     ('lemma_', 'nl_function'),
     ('dep_', 'dobj'),
     ('head.orth_', 'Test'),
     ('head.lemma_', 'test'),
     ('head.pos_', 'VERB')])])
```

And similarly for arguments:

```shell
$ docker-compose -f docker-compose-dev.yml run --rm pynlai \
      pynlai --pipeline nc \
      parse "Test the nl_function with value set to 1."
('to_nc',
 [OrderedDict([
     ('text', 'the nl_function'),
     ('root.orth_', 'nl_function'),
     ('root.lemma_', 'nl_function'),
     ('root.dep_', 'dobj'),
     ('root.head.orth_', 'Test'),
     ('root.head.lemma_', 'test'),
     ('root.head.pos_', 'VERB')]),
  OrderedDict([
     ('text', 'value'),
     ('root.orth_', 'value'),
     ('root.lemma_', 'value'),
     ('root.dep_', 'pobj'),
     ('root.head.orth_', 'with'),
     ('root.head.lemma_', 'with'),
     ('root.head.pos_', 'ADP')])])
```

We can then set up the pynlai triggers and decorate our app function
as follows:

```python

from collections import OrderedDict
import sys

import en_core_web_sm as en

import pynlai
from pynlai import core
from pynlai import views


nlp = en.load()


trigger = pynlai.Trigger(
    core.to_obj,
    views._DEP_TOKEN['HR'],
    OrderedDict([
        ('lemma_', 'nl_function'),
        ('dep_', 'dobj'),
        ('head.lemma_', 'test'),
        ('head.pos_', 'VERB'),
    ]),
)


def arg_callback(sent):
    ents = core.to_ent(doc=sent, nlp=nlp).pop()
    view = core.create_view(ents, views._ENT_SPAN['HR'])
    return dict([('value', view['text'])])


argument = pynlai.Argument(
    core.to_nc,
    views._DEP_SPAN['HR'],
    OrderedDict([
        ('root.lemma_', 'value'),
    ]),
    arg_callback,
)


@pynlai.nl_function(
    trigger,
    argument,
)
def nl_function(value):
    return value
```

And then call our decorated command using a natural language sentence
like so:

```python
nl = 'Test the nl_function with value set to 1.'
pynlai.run(doc=nl, nlp=nlp, obj=sys.modules[__name__])  # returns 1
```
