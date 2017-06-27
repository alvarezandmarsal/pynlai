# -*- coding: utf-8 -*-

'''
cli
---


console script for pynlai.
'''


import pprint
from six.moves import input

import click

from pynlai import core


funcs = {
    'pos': core.sent_to_pos,
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


@main.command()
@click.pass_context
@click.argument('sent', required=False)
def parse(ctx, sent):
    '''
    parse a sentence
    '''

    # this buried import makes unit testing faster
    import en_core_web_sm as en
    nlp = en.load()

    while True:

        sent = input('parse>  ') if ctx.obj['i'] else sent

        try:

            for f in ctx.obj['pipeline']:
                click.echo(pp.pprint(f(sent, nlp)))

            if not ctx.obj['i']:
                break

        except KeyboardInterrupt:
            break


def entry_point():
    '''
    required to make setuptools and click play nicely (context object)
    '''

    return main(obj={})


if __name__ == "__main__":
    entry_point()
