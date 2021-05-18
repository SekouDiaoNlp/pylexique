# -*- coding: utf-8 -*-

"""Main module of pylexique."""

from collections import OrderedDict, defaultdict
from collections.abc import Sequence
import pkg_resources
import json
from math import isnan
# import faster_than_csv as csv
import csv
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
_RESOURCE_PATH_csv = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'Lexique383/Lexique383.txt')
_RESOURCE_PATH_xlsb = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'Lexique383/Lexique383.xlsb')
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

        :return:
            Dictionary with key/values correspondence wit LexItem objects.
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
    All the lexical items are then stored in an Ordered Dict.

    :param lexique_path: string.
        Path to the lexique file.
    :param parser_type: string.
        'pandas_csv', 'std_csv', 'csv' and 'xlsb' are valid values.
    """

    lexique = OrderedDict()
    value_errors = []
    length_errors = []
    lemmes = defaultdict(list)

    def __init__(self, lexique_path: Optional[str] = None, parser_type: str = 'std_csv') -> None:
        self.lexique_path = lexique_path
        if parser_type not in {'xlsb', 'pandas_csv', 'csv', 'std_csv'}:
            raise ValueError(f"The value {parser_type} is not permitted. Only 'pandas_csv', 'std_csv', 'csv' and "
                             f"'xlsb' are valid values.")
        if lexique_path:
            try:
                self._parse_lexique(self.lexique_path, parser_type)
            except UnicodeDecodeError as e:
                raise UnicodeError(f"There was a unicode error while parsing {type(lexique_path)}.") from e
            except FileNotFoundError as e:
                if isinstance(lexique_path, str):
                    raise ValueError(f"Argument 'lexique_path' must be a valid path to Lexique383") from e
                if not isinstance(lexique_path, str):
                    raise TypeError(f"Argument 'lexique_path' must be of type String, not {type(lexique_path)}") from e
        else:
            try:
                # Tries to load the pre-shipped Lexique38X if no path file to the lexicon is provided.
                self._parse_lexique(_RESOURCE_PATH_csv, parser_type)
            except UnicodeDecodeError as e:
                raise UnicodeError(f"There was a unicode error while parsing {type(_RESOURCE_PATH_csv)}.") from e
            except FileNotFoundError as e:
                if isinstance(_RESOURCE_PATH_csv, str):
                    raise ValueError(f"Argument 'lexique_path' must be a valid path to Lexique383") from e
                if not isinstance(_RESOURCE_PATH_csv, str):
                    raise TypeError(f"Argument 'lexique_path'must be of type String, not {type(_RESOURCE_PATH_csv)}") from e
        return

    def __repr__(self) -> str:
        return '{0}.{1}'.format(__name__, self.__class__.__name__)

    def __len__(self) -> int:
        return len(self.lexique)

    @staticmethod
    def _parse_csv(lexique_path: str) -> Generator[list, Any, None]:
        """

        :param lexique_path:
            Path to the lexique file.
        :return: generator of rows:
            Content of the Lexique38x database.
        """
        with open(lexique_path, 'r', encoding='utf-8', errors='ignore') as csv_file:
            raw_content = csv_file.readlines()
            content = (row.strip().split('\t') for row in raw_content[1:])
            return content

    def _parse_lexique(self, lexique_path: Optional[str], parser_type: str) -> None:
        """
        | Parses the given lexique file and creates 2 hash tables to store the data.

        :param lexique_path: string.
            Path to the lexique file.
        :param parser_type: string.
            Can be either 'csv', 'pandas_csv', 'std_csv' or 'xlsb'.
        :return:
        """
        try:
            if parser_type == 'xlsb':
                df = pd.read_excel(lexique_path, engine='pyxlsb')
                content = (list(row) for row in df.values)
            elif parser_type == 'pandas_csv':
                df = pd.read_csv(lexique_path, delimiter='\t')
                content = (list(row) for row in df.values)
            elif parser_type == 'csv':
                content = self._parse_csv(lexique_path)
            elif parser_type == 'std_csv':
                raw_content = csv.reader(lexique_path, delimiter='\t')
                raw_content.__next__()
                content = raw_content
            else:
                content = self._parse_csv(lexique_path)
        except UnicodeDecodeError:
            logger.warn(f"there was an issue while parsing the file {lexique_path}."
                        f" Trying again with built-in csv parser")
            content = self._parse_csv(lexique_path)
        self._create_db(content)
        if self.value_errors:
            self._save_errors(self.value_errors, _VALUE_ERRORS_PATH)
        if self.length_errors:
            self._save_errors(self.length_errors, _LENGTH_ERRORS_PATH)
        return

    def _create_db(self, lexicon: Generator[list, Any, None]) -> None:
        """
        | Creates 2 hash tables populated with the entries in lexique if it does not exist yet.
        | One hash table holds the LexItems, the other holds the same data but grouped by lemmma to give access to all lexical forms of a word.

        :param lexicon: Iterable.
            Iterable containing the lexique383 entries.
        :return:
        """
        for row in lexicon:
            try:
                converted_row_fields = self._convert_entries(row)
            except ValueError:
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
            List of column entries representing a row.
        :return: typed_row_fields:
            List of typed column entries representing a typed row.
        """
        errors = defaultdict(list)
        converted_row_fields = []
        for attr, value in zip(LEXIQUE383_FIELD_NAMES, row_fields):
            if isinstance(value, float) and isnan(value):
                value = ''
            if attr in {'freqlemfilms2', 'freqlemlivres', 'freqfilms2', 'freqlivres', 'old20', 'pld20'}:
                if not isinstance(value, float):
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

    def get_lex(self, words: Union[Tuple[str], str]) -> OrderedDict:
        """
        Recovers the lexical entries for the words in the sequence

        :param words:
            A string or a tuple of multiple strings for getting the LexItems for multiple words.
        :return:
            Dictionary of LexItems.
        """
        results = OrderedDict()
        if isinstance(words, str):
            try:
                results[words] = self.lexique[words.lower()]
            except AttributeError:
                logger.warning('the word {} is not in Lexique383'.format(words))
        elif isinstance(words, Sequence):
            for word in words:
                if isinstance(word, str):
                    try:
                        results[word] = self.lexique[word.lower()]
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
            String.
        :return:
            List of LexItem objects sharing the same root lemma.
        """
        try:
            lex_entry = self.lexique[word.lower()]
        except ValueError as e:
            logger.warning('The word {} is not in Lexique383\n'.format(word))
            raise ValueError from e
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

        :param errors:
            List of errors encountered while parsing Lexique38x
        :param errors_path:
            Path to save the errors.
        :return:

        """
        with open(errors_path, 'w', encoding='utf-8') as json_file:
            json.dump(errors, json_file, indent=4)
        return


if __name__ == "__main__":
    pass
