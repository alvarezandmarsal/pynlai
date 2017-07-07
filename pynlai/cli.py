# -*- coding: utf-8 -*-

'''
cli
---


console script for pynlai.
'''


import pprint
from six.moves import input

import click
import en_core_web_sm as en

from pynlai.core import (
    create_view,
    to_ent,
    to_nc,
    to_obj,
    to_pos,
    to_sub,
)

from pynlai.views import (
    _DEP_SPAN,
    _DEP_TOKEN,
    _ENT_SPAN,
    _POS_TOKEN,
)


func_view = {
    'ent': (to_ent, _ENT_SPAN['HR']),
    'nc': (to_nc, _DEP_SPAN['HR']),
    'obj': (to_obj, _DEP_TOKEN['HR']),
    'pos': (to_pos, _POS_TOKEN['HR']),
    'sub': (to_sub, _DEP_TOKEN['HR']),
}

pp = pprint.PrettyPrinter(indent=2, width=240)


@click.group()
@click.pass_context
@click.option(
    '--interactive', '-i',
    is_flag=True,
    help='interactive prompt for sentence input'
)
@click.option(
    '--pipeline',
    default=('pos',),
    multiple=True,
    type=click.Choice(func_view.keys()),
    help='function(s) and view(s) to use for processing pipeline'
)
def main(ctx, interactive, pipeline):
    '''
    pynlai command line interface
    '''

    ctx.obj['i'] = interactive
    ctx.obj['pipeline'] = [func_view[k] for k in pipeline]
    ctx.obj['nlp'] = en.load()


@main.command()
@click.pass_context
@click.argument('sent', required=False)
def parse(ctx, sent):
    '''
    parse a sentence
    '''

    nlp = ctx.obj['nlp']

    while True:

        sent = input('parse>  ') if ctx.obj['i'] else sent

        try:

            for f, v in ctx.obj['pipeline']:
                r = [create_view(e, v) for e in f(doc=sent, nlp=nlp)]
                click.echo(pp.pprint((f.__name__, r)))

            if not ctx.obj['i']:
                break

        except KeyboardInterrupt:
            break


@main.command()
@click.pass_context
@click.argument('file')
def parsefile(ctx, file):
    '''
    parse a document
    '''

    nlp = ctx.obj['nlp']

    with open(file, 'r') as f:

        doc = nlp(f.read())

        for sent in doc.sents:
            click.echo(sent.text)
            ctx.invoke(parse, sent=sent.text)


def entry_point():
    '''
    required to make setuptools and click play nicely (context object)
    '''

    return main(obj={})


if __name__ == "__main__":
    entry_point()
