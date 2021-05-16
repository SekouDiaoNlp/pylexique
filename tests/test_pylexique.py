#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pylexique` package."""

import pytest
import json
from click.testing import CliRunner
from pprint import pprint
import pkg_resources
import sys
from pylexique import Lexique383
from time import time

from pylexique import pylexique, cli
from py._path.local import LocalPath

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

# Assigns resource paths
_RESOURCE_PACKAGE = 'pylexique'

_RESOURCE_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'Lexique383/Lexique383.xlsb')
_RESOURCE_PATH_csv = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'Lexique383/Lexique383.txt')


class Test_Load_Times:

    def test_load_times(self):
        #  Create new Lexique383 instance with a pre-built Lexique383.
        t0 = time()
        lexicon = Lexique383()
        t1 = time() - t0
        print(f'Parsing csv with standard lib csv parser took {round(t1, 2)} seconds\n')
        # Creates a new Lexique383 instance while supplying your own Lexique38X lexicon.

        t4 = time()
        lexicon1 = Lexique383(_RESOURCE_PATH_csv, parser_type='csv')
        t5 = time() - t4
        print(f'Parsing csv with built-in csv parser took {round(t5, 2)} seconds\n')

        t6 = time()
        lexicon2 = Lexique383(_RESOURCE_PATH_csv, parser_type='pandas_csv')
        t7 = time() - t6
        print(f'Parsing csv with pandas csv parser took {round(t7, 2)} seconds\n')

        t2 = time()
        lexicon3 = Lexique383(_RESOURCE_PATH, parser_type='xlsb')
        t3 = time() - t2
        print(f'Parsing xlsb with pandas+pyxlsb took {round(t3, 2)} seconds\n')
        print('ok')
        return


class TestAll:

    lexicon = Lexique383()

    def test_all(self) -> None:
        # There are 2 ways to access the lexical information of a word:
        # Either use the utility method Lexique383.get_lex(item)
        # Or you can directly access the lexicon directory through lexicon.lexique[item] .
        with pytest.raises(ValueError):
            LEXIQUE = Lexique383('random.csv', parser_type='csv')

        with pytest.raises((ValueError, OSError)):
            LEXIQUE = Lexique383(42, parser_type='csv')

        #  Retrieves the lexical information of 'abaissait' and 'a'.
        var_1 = self.lexicon.lexique['abaissait']
        var_1_bis = self.lexicon.get_lex('abaissait')

        # Check both objects are the same
        var_1_equality = var_1 == var_1_bis['abaissait']
        print(var_1_equality)

        # Because in French the world 'a' is very polysemic word, it has several entries in Lexique 383.
        # For this reason the lexicon Dict has the value of the `ortho` property of its LexicalEntry.
        # In th case of 'abaissait' there is only one LexicalItem corresponding to this dist key.
        # But in the case of 'a' there are several LexItem objects corresponding to this key and then the LexItem objects
        # are stored in a list corresponding to th value of the key.
        var_2 = self.lexicon.lexique['a']
        var_2_bis = self.lexicon.get_lex('a')

        # Check both objects are the same
        var_2_equality = var_2 == var_2_bis['a']
        print(var_2_equality)

        # Retrieving the lexical information of several words by passing a Sequence of strings

        var_multiple = self.lexicon.get_lex(('il', 'mange', 'une', 'baguette'))
        pprint(var_multiple)

        # gets all forms with a common lemma
        all_forms = self.lexicon.get_all_forms('allions')

        # You can use the method LexItem.to_dict() to produce a dictionary with key/value pairs corresponding to the LexItem

        print('\n\n')
        if isinstance(var_1, list):
            for elmt in var_1:
                pprint(elmt.to_dict())
                print('\n\n')
        else:
            pprint(var_1.to_dict())
            print('\n\n')

        print('\n\n')
        if isinstance(var_2, list):
            for elmt in var_2:
                pprint(elmt.to_dict())
                print('\n\n')
        else:
            pprint(var_2.to_dict())
            print('\n\n')

        # Get all verbs in the DataSet. Because some words have the same orthography, some keys of the dictionary
        # don't have a unique LexItem object as their value, but a list of those.
        verbs = []
        for x in self.lexicon.lexique.values():
            if isinstance(x, list):
                for y in x:
                    if not isinstance(y, list) and y.cgram == 'VER':
                        verbs.append(y)
            elif x.cgram == 'VER':
                verbs.append(x)
            else:
                continue

        print('Printing the first 5 verbs found in the preceding search:')
        pprint(verbs[0:5])

        # Print the first 5 verbs with full lexical information.
        for verb in verbs[0:5]:
            pprint(verb.to_dict())
        pass

    def test_content(self) -> None:
        """Sample pytest test of pylexique."""
        others = []
        x = 'a posteriori'
        if x in self.lexicon.lexique:
            if isinstance(self.lexicon.lexique[x], list):
                for elmnt in self.lexicon.lexique[x]:
                    if elmnt.cgram == 'ADV':
                        assert elmnt.cgram == 'ADV'
            elif self.lexicon.lexique[x].cgram == 'ADV':
                assert self.lexicon.lexique[x].cgram == 'ADV'
            else:
                others.append(x)


class TestCLI:

    def test_command_line_interface(self) -> None:
        """Test the CLI."""
        word = 'allons'
        runner = CliRunner()
        result = runner.invoke(cli.main, [word])
        assert result.exit_code == 0
        assert 'aller' in result.output
        all_results = runner.invoke(cli.main, [word, '-a'])
        # assert all_results.exit_code == 0
        assert 'Retrieving all the lexical forms of the supplied words.' in all_results.output
        # assert 'allions' in all_results.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert 'Pylexique is a Python wrapper around Lexique83.' in help_result.output

    def test_save_file(self, tmpdir: LocalPath) -> None:
        """
        Tests file saving feature.

        """
        # test_verb = lexicon.lexique['aller']
        path = tmpdir.mkdir("sub").join('results.json')
        verb = 'aller'
        runner = CliRunner()
        result = runner.invoke(cli.main, [verb, '-o', path])
        assert result.exit_code == 0
        my_file = Path(path)
        assert my_file.is_file()
        with open(my_file, encoding='utf-8') as file:
            output = json.load(file)
        # assert test_verb[0] in output['aller'][0]
