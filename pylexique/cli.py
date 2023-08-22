# -*- coding: utf-8 -*-

"""Console CLI script for pylexique."""
import sys
import click
import json
import logging
from rich.console import Console
from rich.table import Table
from pylexique import Lexique383, LexItem
from collections import defaultdict
from typing import Sequence, Dict


LEXIQUE383_FIELD_NAMES = ['ortho', 'phon', 'lemme', 'cgram', 'genre', 'nombre', 'freqlemfilms2', 'freqlemlivres',
                          'freqfilms2', 'freqlivres', 'infover', 'nbhomogr', 'nbhomoph', 'islem', 'nblettres',
                          'nbphons', 'cvcv', 'p_cvcv', 'voisorth', 'voisphon', 'puorth', 'puphon', 'syll', 'nbsyll',
                          'cv_cv', 'orthrenv', 'phonrenv', 'orthosyll', 'cgramortho', 'deflem', 'defobs', 'old20',
                          'pld20', 'morphoder', 'nbmorph']

def convert_to_dict(obj: LexItem) -> Dict:
    if isinstance(obj, LexItem):
        return obj.to_dict()
    return obj

@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument('words', nargs=-1)
@click.option('-a', '--all_forms',
              is_flag=True,
              help="Gets all lexical forms of a given word. Only takes 1 word as an argument.")
@click.option('-o', '--output',
              default=None,
              help="Path of the json filename for storing the lexical entries.",
              type=click.STRING)
def main(words: Sequence[str], all_forms: bool, output: str) -> None:
    """Pylexique is a Python wrapper around Lexique83.
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
    results = defaultdict(list)
    for word in words:
        if all_forms:
            results[word].append(LEXIQUE.get_all_forms(word))
        else:
            results[word].append(LEXIQUE.lexique[word])

    console = Console()

    for word, elements in results.items():
        table = Table(title=f"Lexical Information for '{word}'", show_header=True)
        table.add_column("Attribute", style="bold")

        num_columns = 1  # Initialize the number of columns
        for element in elements:
            if isinstance(element, LexItem):
                num_columns += 1
                table.add_column(element.lemme, justify="center")  # Add a column for each LexItem
                element_dict = element.to_dict()
                for field in LEXIQUE383_FIELD_NAMES:
                    value = element_dict.get(field, "")
                    table.add_row(field, str(value), *[None] * (num_columns - 2))  # Add None values for other columns
            else:
                for item in element:
                    if isinstance(item, LexItem):
                        num_columns += 1
                        table.add_column(item.lemme, justify="center")  # Add a column for each LexItem
                        item_dict = item.to_dict()
                        for field in LEXIQUE383_FIELD_NAMES:
                            value = item_dict.get(field, "")
                            table.add_row(field, *[None] * (num_columns - 2), str(value))  # Add None values for other columns

        console.print(table)

    if output:
        with open(output, 'w', encoding='utf-8') as file:
            json.dump(results, file, indent=4, ensure_ascii=False, default=convert_to_dict)
            console.print(f"The Lexical Items have been successfully saved to {output} by pylexique.")

if __name__ == "__main__":
    main()  # pragma: no cover
