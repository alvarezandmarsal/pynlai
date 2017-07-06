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

from pynlai import core


funcs = {
    'dep': core.to_dep,
    'ent': core.to_ent,
    'obj': core.to_obj,
    'pos': core.to_pos,
    'sub': core.to_sub,
}

pp = pprint.PrettyPrinter(indent=4)


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
    type=click.Choice(funcs.keys()),
    help='function(s) to use for processing pipeline'
)
def main(ctx, interactive, pipeline):
    '''
    pynlai command line interface
    '''

    pipeline = [funcs[k] for k in pipeline]
    ctx.obj['i'] = interactive
    ctx.obj['pipeline'] = pipeline
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

            for f in ctx.obj['pipeline']:
                click.echo(pp.pprint(f(sent=sent, nlp=nlp)))

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
