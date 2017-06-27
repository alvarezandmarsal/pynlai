# -*- coding: utf-8 -*-

'''
cli
---


console script for pynlai.
'''


import pprint

import click
import en_core_web_sm as en

from pynlai import core


funcs = {
    'pos': core.sent_to_pos,
}
nlp = en.load()
pp = pprint.PrettyPrinter(indent=4)


@click.group()
@click.option(
    '--pipeline',
    default=('pos',),
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

    for f in ctx.obj['pipeline']:
        click.echo(pp.pprint(f(sent, nlp)))


def entry_point():
    '''
    required to make setuptools and click play nicely (context object)
    '''

    return main(obj={})


if __name__ == "__main__":
    entry_point()
