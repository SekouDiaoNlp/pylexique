# -*- coding: utf-8 -*-

"""Main module of pylexique."""

from collections import OrderedDict, defaultdict
from collections.abc import Sequence
import pkg_resources
import json
import sys
# import faster_than_csv as csv

import pandas as pd
from dataclasses import dataclass
from typing import DefaultDict, Dict, List, Optional, Tuple, Union, Generator, Any

__all__ = ['Lexique383', 'LexItem', 'LexEntryTypes']

try:
    from utils import logger
except ModuleNotFoundError or ImportError:
    from .utils import logger

_RESOURCE_PACKAGE = __name__

HOME_PATH = '/'.join(('Lexique', ''))
_RESOURCE_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'Lexique383/Lexique383.txt')
_VALUE_ERRORS_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'errors/value_errors.json')
_LENGTH_ERRORS_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'errors/length_errors.json')

LEXIQUE383_FIELD_NAMES = ['ortho', 'phon', 'lemme', 'cgram', 'genre', 'nombre', 'freqlemfilms2', 'freqlemlivres',
                          'freqfilms2',
                          'freqlivres', 'infover', 'nbhomogr', 'nbhomoph', 'islem', 'nblettres', 'nbphons', 'cvcv',
                          'p_cvcv',
                          'voisorth', 'voisphon', 'puorth', 'puphon', 'syll', 'nbsyll', 'cv_cv', 'orthrenv', 'phonrenv',
                          'orthosyll', 'cgramortho', 'deflem', 'defobs', 'old20', 'pld20', 'morphoder', 'nbmorph']


@dataclass(init=True, repr=False, eq=True, order=False, unsafe_hash=False, frozen=True)
class LexEntryTypes:
    """
    Type information about all the lexical attributes in a LexItem object.

    """
    ortho: str
    phon: str
    lemme: str
    cgram: str
    genre: str
    nombre: str
    freqlemfilms2: float
    freqlemlivres: float
    freqfilms2: float
    freqlivres: float
    infover: str
    nbhomogr: int
    nbhomoph: int
    islem: bool
    nblettres: int
    nbphons: int
    cvcv: str
    p_cvcv: str
    voisorth: int
    voisphon: int
    puorth: int
    puphon: int
    syll: str
    nbsyll: int
    cv_cv: str
    orthrenv: str
    phonrenv: str
    orthosyll: str
    cgramortho: str
    deflem: float
    defobs: int
    old20: float
    pld20: float
    morphoder: str
    nbmorph: int


@dataclass(init=True, repr=False, eq=True, order=False, unsafe_hash=False, frozen=True)
class LexItem(LexEntryTypes):
    """
    | This class defines the lexical items in Lexique383.
    | It uses slots for memory efficiency.

    """
    _s = LEXIQUE383_FIELD_NAMES
    __slots__ = _s

    def __repr__(self) -> str:
        return '{0}({1}, {2}, {3})'.format(self.__class__.__name__, self.ortho, self.lemme, self.cgram)

    def to_dict(self) -> OrderedDict:
        """
        | Converts the LexItem to a dict containing its attributes and their values

        :return: Dictionary with key/values correspondence wit LexItem objects
        """
        attributes = []
        for attr in self.__slots__:
            try:
                value = getattr(self, attr)
            except AttributeError as e:
                logger.warning(e)
                continue
            attributes.append((attr, value))
        result = OrderedDict(attributes)
        return result


class Lexique383:
    """
    This is the class handling the lexique database.
    It provides methods for interacting with the Lexique DB
    and retrieve lexical items.
    All the lexical items are then stored in an Ordered Dict called

    :param lexique_path: string.
        Path to the lexique csv file.
    """

    lexique = OrderedDict()
    value_errors = []
    length_errors = []
    lemmes = defaultdict(list)

    def __init__(self, lexique_path: Optional[str] = None) -> None:
        self.lexique_path = lexique_path
        if lexique_path:
            try:
                self._parse_lexique(self.lexique_path)
            except UnicodeDecodeError:
                sys.exit(0)
            except FileNotFoundError:
                if isinstance(lexique_path, str):
                    raise ValueError(f"Argument 'lexique_path' must be a valid path to Lexique383")
                if not isinstance(lexique_path, str):
                    raise TypeError(f"Argument 'lexique_path' must be of type String, not {type(lexique_path)}")
        else:
            try:
                # Tries to load the pre-shipped Lexique38X if no path file to the lexicon is provided.
                self._parse_lexique(_RESOURCE_PATH)
            except UnicodeDecodeError:
                sys.exit(0)
            except FileNotFoundError:
                if isinstance(_RESOURCE_PATH, str):
                    raise ValueError(f"Argument 'lexique_path' must be a valid path to Lexique383")
                if not isinstance(_RESOURCE_PATH, str):
                    raise TypeError(f"Argument 'lexique_path'must be of type String, not {type(_RESOURCE_PATH)}")
        return

    def __repr__(self):
        return '{0}.{1}'.format(__name__, self.__class__.__name__)

    def __len__(self):
        return len(self.lexique)

    def _parse_lexique(self, lexique_path: str) -> None:
        """
        | Parses the given lexique file and creates a hdf5 table to store the data.

        :param lexique_path: string.
            Path to the lexique csv file.
        :return:
        """
        # Create a dataframe from csv
        try:
            df = pd.read_csv(lexique_path, delimiter='\t')
        except UnicodeDecodeError:
            logger.warn('there was an issue while parsing the file {0}'.format(lexique_path))
            raise UnicodeDecodeError
        # Generator comprehension to create a list of lists from Dataframe rows
        content = (list(row) for row in df.values)
        self._create_db(content)
        if self.value_errors:
            self._save_errors(self.value_errors, _VALUE_ERRORS_PATH)
        if self.length_errors:
            self._save_errors(self.length_errors, _LENGTH_ERRORS_PATH)
        return

    def _create_db(self, lexicon: Generator[list, Any, None]) -> None:
        """
        | Creates an hash table populated with the entries in lexique if it does not exist yet.
        | It stores the hash table database for fast access.

        :param lexicon: Iterable.
            Iterable containing the lexique383 entries.
        :return:
        """
        for row in lexicon:
            try:
                converted_row_fields = self._convert_entries(row)
            except ValueError as e:
                continue
            lexical_entry = LexItem(*converted_row_fields)
            self.lemmes[lexical_entry.lemme].append(lexical_entry)
            if converted_row_fields[0] in self.lexique and not isinstance(self.lexique[converted_row_fields[0]], list):
                self.lexique[converted_row_fields[0]] = [self.lexique[converted_row_fields[0]]]
                self.lexique[converted_row_fields[0]].append(lexical_entry)
            elif converted_row_fields[0] in self.lexique and isinstance(self.lexique[converted_row_fields[0]], list):
                self.lexique[converted_row_fields[0]].append(lexical_entry)
            else:
                self.lexique[converted_row_fields[0]] = lexical_entry
        return

    def _convert_entries(self, row_fields: Union[List[str], List[Union[str, float, int, bool]]]) -> List[Union[str, float, int, bool]]:
        """
        | Convert entries from `strings` to `int`, `bool` or `float` and generates
        | a new list with typed entries.

        :param row_fields:
        :return: converted_row_fields:
        """
        errors = defaultdict(list)
        converted_row_fields = []
        for attr, value in zip(LEXIQUE383_FIELD_NAMES, row_fields):
            if isinstance(value, float):
                value = ''
            if attr in {'freqlemfilms2', 'freqlemlivres', 'freqfilms2', 'freqlivres', 'old20', 'pld20'}:
                if (value != '' or value != ' ') and ',' in value:
                    value = value.replace(',', '.')
                    value = float(value)
            if attr == 'islem':
                if isinstance(value, str):
                    value = value.strip()
                if value != '' and value not in ('0', '1', 0, 1):
                    value = 0
                try:
                    value = bool(int(value))
                except ValueError:
                    errors[row_fields[0]].append({attr: value})
                    value = value
                    self.value_errors.append(errors)
            if attr in {'nbhomogr', 'nbhomoph', 'nblettres', 'nbphons',
                        'voisorth', 'voisphon', 'puorth', 'puphon', 'nbsyll'}:
                if value != '' or value != ' ':
                    try:
                        value = int(value)
                    except ValueError:
                        errors[row_fields[0]].append({attr: value})
                        value = value
                        self.value_errors.append(errors)
            converted_row_fields.append(value)
        if len(converted_row_fields) != 35:
            self.length_errors.append((converted_row_fields, row_fields))
            raise ValueError
        else:
            row_fields = converted_row_fields
        return row_fields

    def get_lex(self, words: Union[Tuple[str, str, str, str], str]) -> OrderedDict:
        """
        Recovers the lexical entries for the words in the sequence

        :param words:
        :return: Dictionary of LexItems:
        """
        results = OrderedDict()
        if isinstance(words, str):
            try:
                results[words] = self.lexique[words]
            except AttributeError:
                logger.warning('the word {} is not in Lexique383'.format(words))
        elif isinstance(words, Sequence):
            for word in words:
                if isinstance(word, str):
                    try:
                        results[word] = self.lexique[word]
                    except AttributeError:
                        logger.warning('The word {} is not in Lexique383\n'.format(word))
                        continue
                else:
                    logger.warning('{} is not a valid string'.format(word))
                    raise TypeError
        else:
            raise TypeError
        return results

    def get_all_forms(self, word: str) -> List[LexItem]:
        """
        Gets all lexical forms of a given word.

        :param word:
        :return: List of LexItem objects sharing the same root lemma.
        """
        try:
            lex_entry = self.lexique[word]
        except ValueError as e:
            logger.warning('The word {} is not in Lexique383\n'.format(word))
            raise ValueError
        if isinstance(lex_entry, LexItem):
            lemmes = self.lemmes[lex_entry.lemme]
        elif isinstance(lex_entry, OrderedDict):
            lemmes = self.lemmes[lex_entry['lemme']]
        elif isinstance(lex_entry, list):
            lemmes = self.lemmes[lex_entry[0].lemme]
        else:
            raise TypeError
        return lemmes

    @staticmethod
    def _save_errors(errors: Union[
        List[Tuple[List[Union[str, float, int, bool]], List[str]]], List[DefaultDict[str, List[Dict[str, str]]]]],
                     errors_path: str) -> None:
        """
        Saves the mismatched key/values in Lexique383 based on type coercion.

        """
        with open(errors_path, 'w', encoding='utf-8') as json_file:
            json.dump(errors, json_file, indent=4)
        return


if __name__ == "__main__":
    pass
