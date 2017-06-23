# -*- coding: utf-8 -*-

'''
cli
---


console script for pynlai.
'''


import pprint

import click
import spacy
import en_core_web_sm as en

from pynlai import core


funcs = {
    'sent_to_pos': core.sent_to_pos,
}
nlp = en.load()
pp = pprint.PrettyPrinter(indent=4)


@click.group()
@click.option(
    '--pipeline',
    default=('sent_to_pos',),
    multiple=True,
    type=click.Choice(funcs.keys()),
    help='function(s) to use for processing pipeline',
)
@click.pass_context
def main(ctx, pipeline):
    '''
    pynlai command line interface
    '''

    pipeline = [funcs[k] for k in pipeline]
    ctx.obj['pipeline'] = pipeline


@main.command()
@click.argument('sent')
@click.pass_context
def parse(ctx, sent):
    '''
    parse a sentence
    '''

    click.echo(pp.pprint([r(sent) for r in ctx.obj['pipeline']]))


if __name__ == "__main__":
    main(obj={})
