# -*- coding: utf-8 -*-

"""Console script for pylexique."""
import sys
import click
import json
import logging
from .pylexique import Lexique383


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument('words', nargs=-1)
@click.option('-o', '--output',
              default=None,
              help=_("Path of the filename for storing the lexical entries"),
              type=click.STRING)
def main(words, output):
    """Pylexique is a Python wrapper around Lexique83_.
    It allows to extract lexical information from more than 140 000 French words in an Object Oriented way.


    * Free software: MIT license
    * Documentation: https://pylexique.readthedocs.io.
    """
    logger = logging.getLogger(__name__)

    # create console handler and set level to debug
    console_handler = logging.StreamHandler(sys.stdout)
    error_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.INFO)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(console_handler)
    logger.addHandler(error_handler)
    logger.setLevel(logging.INFO)

    LEXIQUE = Lexique383()
    results = {}
    for word in words:
        results[word] = LEXIQUE.lexique[word]
    if output:
        with open(output, 'w', encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
            print('The Lexical Items have been successfully saved to {0}.'.format(output))
    else:
        print(json.dumps(results, ensure_ascii=False, indent=4))
    return


if __name__ == "__main__":
    main()  # pragma: no cover
