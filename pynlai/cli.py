# -*- coding: utf-8 -*-

'''
cli
---


console script for pynlai.
'''


import click


@click.command()
def main(args=None):
    '''
    pynlai command line interface
    '''

    click.echo("update pynlai.cli.main")


if __name__ == "__main__":
    main()
