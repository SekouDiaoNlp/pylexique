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
from typing import Sequence, Dict, Union, List, DefaultDict

LEXIQUE383_FIELD_NAMES = ['ortho', 'phon', 'lemme', 'cgram', 'genre', 'nombre', 'freqlemfilms2', 'freqlemlivres',
                          'freqfilms2',
                          'freqlivres', 'infover', 'nbhomogr', 'nbhomoph', 'islem', 'nblettres', 'nbphons', 'cvcv',
                          'p_cvcv',
                          'voisorth', 'voisphon', 'puorth', 'puphon', 'syll', 'nbsyll', 'cv_cv', 'orthrenv', 'phonrenv',
                          'orthosyll', 'cgramortho', 'deflem', 'defobs', 'old20', 'pld20', 'morphoder', 'nbmorph', 'sorted_ortho']
def convert_to_dict(obj: LexItem) -> Dict[str, Union[str, float, int, bool]]:
    if isinstance(obj, LexItem):
        return obj.to_dict()
    return obj

def _display_results(console: Console, results: DefaultDict[str, List[Union[LexItem, List[LexItem]]]], output: str) -> None:
    """Display lexical results using rich tables."""
    for word, elements in results.items():
        if not elements:
            console.print(f"The word {word} was not found in Lexique383.")
            continue
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

@click.command(context_settings=dict(help_option_names=["-h", "--help"])) #type: ignore
@click.argument('words', nargs=-1) #type: ignore
@click.option('-a', '--all_forms', #type: ignore
              is_flag=True,
              help="Gets all lexical forms of a given word. Only takes 1 word as an argument.")
@click.option('-o', '--output', #type: ignore
              default=None,
              help="Path of the json filename for storing the lexical entries.",
              type=click.STRING)
@click.option('-i', '--interactive', is_flag=True, help="Enter interactive mode to input words and options interactively.") #type: ignore
def main(words: Sequence[str], all_forms: bool, output: str, interactive: bool) -> None:
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
    
    if interactive:
        _run_interactive_mode(LEXIQUE, output)
    else:
        _run_batch_mode(LEXIQUE, words, all_forms, output)

def _run_interactive_mode(lexique: Lexique383, output: str) -> None:
    """Run the interactive mode for pylexique."""
    console = Console()
    cached_results: Dict[str, DefaultDict[str, List[Union[LexItem, List[LexItem]]]]] = {}

    while True:
        word = click.prompt("Enter a word (or press Ctrl+C to quit):", type=str)
        
        try:
            if word in cached_results:
                results = cached_results[word]
            else:
                all_forms = click.confirm("Get all forms of the word?")
                results = _get_results(lexique, [word], all_forms)
                cached_results[word] = results

            _display_results(console, results, output)
        except KeyboardInterrupt:
            console.print("\nExiting interactive mode.")
            break

def _run_batch_mode(lexique: Lexique383, words: Sequence[str], all_forms: bool, output: str) -> None:
    """Run the batch mode for pylexique."""
    console = Console()
    results = _get_results(lexique, words, all_forms)
    _display_results(console, results, output)

def _get_results(lexique: Lexique383, words: Sequence[str], all_forms: bool) -> DefaultDict[str, List[Union[LexItem, List[LexItem]]]]:
    """Get lexical results for the provided words."""
    results: DefaultDict[str, List[Union[LexItem, List[LexItem]]]] = DefaultDict(list)
    for word in words:
        lex_items = lexique.get_lex(word).get(word, [])
        if lex_items:
            if all_forms:
                results[word].append(lexique.get_all_forms(word))
            else:
                results[word].append(lex_items)
        else:
            results[word] = []
    return results

if __name__ == "__main__":
    main()  # pragma: no cover
