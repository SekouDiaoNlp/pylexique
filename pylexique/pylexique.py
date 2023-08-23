"""Main module of pylexique."""

from collections import OrderedDict, defaultdict
from collections.abc import Sequence
import pkg_resources
import pickle
import json
from math import isnan
# import faster_than_csv as csv
import csv
from csv import reader
import pandas as pd
from dataclasses import dataclass
from typing import DefaultDict, Dict, List, Optional, Tuple, Union, Generator, Any, Iterator

__all__ = ['Lexique383', 'LexItem', 'LexEntryTypes']

try:
    from utils import logger
except (ModuleNotFoundError, ImportError):
    from .utils import logger

_RESOURCE_PACKAGE = __name__

HOME_PATH = '/'.join(('Lexique', ''))
_RESOURCE_PATH_csv = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'Lexique383/Lexique383.txt')
_CACHE_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'Lexique383/Lexique383.pkl')
_VALUE_ERRORS_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'errors/value_errors.json')
_LENGTH_ERRORS_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'errors/length_errors.json')

LEXIQUE383_FIELD_NAMES = ['ortho', 'phon', 'lemme', 'cgram', 'genre', 'nombre', 'freqlemfilms2', 'freqlemlivres',
                          'freqfilms2',
                          'freqlivres', 'infover', 'nbhomogr', 'nbhomoph', 'islem', 'nblettres', 'nbphons', 'cvcv',
                          'p_cvcv',
                          'voisorth', 'voisphon', 'puorth', 'puphon', 'syll', 'nbsyll', 'cv_cv', 'orthrenv', 'phonrenv',
                          'orthosyll', 'cgramortho', 'deflem', 'defobs', 'old20', 'pld20', 'morphoder', 'nbmorph']

ConvertedRow = Tuple[str, str, str, str, str, str, float, float, float, float, str, int, int, bool,
                     int, int, str, str, int, int, int, int, str, int, str, str, str, str, str, float,
                     int, float, float, str, int]


@dataclass(init=True, repr=False, eq=True, order=False, unsafe_hash=False)
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


@dataclass(init=True, repr=False, eq=True, order=False, unsafe_hash=False)
class LexItem(LexEntryTypes):
    """
    | This class defines the lexical items in Lexique383.
    | It uses slots for memory efficiency.

    """
    _s = LEXIQUE383_FIELD_NAMES
    __slots__ = _s

    def __repr__(self) -> str:
        return '{0}({1}, {2}, {3})'.format(self.__class__.__name__, self.ortho, self.lemme, self.cgram)

    def to_dict(self) -> Dict[str, Union[str, float, int, bool]]:
        """
        | Converts the LexItem to a dict containing its attributes and their values

        :return: OrderedDict.
            Dictionary with key/values correspondence wit LexItem objects.
        :raises: AttributeError.
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
        'pandas_csv' and 'csv' are valid values. 'csv' is the default value.
    :cvar lexique: Dictionary containing all the LexicalItem objects indexed by orthography.
    :cvar lemmes: Dictionary containing all the LexicalItem objects indexed by lemma.
    :cvar anagrams: Dictionary containing all the LexicalItem objects indexed by anagram form.
    """

    lexique: Dict[str, Any] = OrderedDict()
    value_errors: List[Any] = []
    length_errors: List[Any] = []
    lemmes: Dict[str, List[LexItem]] = defaultdict(list)
    anagrams: Dict[str, List[LexItem]] = defaultdict(list)

    def __init__(self, lexique_path: Optional[str] = _RESOURCE_PATH_csv, parser_type: str = 'csv') -> None:
        self.lexique_path = lexique_path

        try:
            self.load_cache()
        except FileNotFoundError:
            logger.info("Cached Lexique383 not found. Parsing the lexique file...")
            self._parse_lexique(lexique_path, parser_type)
            self.save_cache()

    def load_cache(self) -> None:
        """Load cached Lexique383 from disk."""
        try:
            with open(_CACHE_PATH, "rb") as cache_file:
                cached_lexique = pickle.load(cache_file)
                self.lexique.update(cached_lexique["lexique"])
                self.lemmes.update(cached_lexique["lemmes"])
                self.anagrams.update(cached_lexique["anagrams"])
                self.value_errors.extend(cached_lexique["value_errors"])
                self.length_errors.extend(cached_lexique["length_errors"])
        except FileNotFoundError:
            raise

    def save_cache(self) -> None:
        """Save Lexique383 to cache on disk."""
        cached_lexique = {
            "lexique": self.lexique,
            "lemmes": self.lemmes,
            "anagrams": self.anagrams,
            "value_errors": self.value_errors,
            "length_errors": self.length_errors
        }
        with open(_CACHE_PATH, "wb") as cache_file:
            pickle.dump(cached_lexique, cache_file)

    def __repr__(self) -> str:
        return '{0}.{1}'.format(__name__, self.__class__.__name__)

    def __len__(self) -> int:
        return len(self.lexique)

    @staticmethod
    def _parse_csv(lexique_path: str) -> Generator[list, Any, None]:    #type: ignore[type-arg]
        """

        :param lexique_path: string.
            Path to the lexique file.
        :return: generator of rows:
            Content of the Lexique38x database.
        """
        with open(lexique_path, 'r', encoding='iso-8859-1') as csv_file:
            raw_content = csv_file.readlines()
            content = (row.strip().split('\t') for row in raw_content[1:])
            return content

    def _parse_lexique(self, lexique_path: str, parser_type: str) -> None:
        """
        | Parses the given lexique file and creates 2 hash tables to store the data.

        :param lexique_path: string.
            Path to the lexique file.
        :param parser_type: string.
            Can be either 'csv', 'pandas_csv'.
        :return:
        """
        try:
            if parser_type == 'pandas_csv':
                df = pd.read_csv(lexique_path, delimiter='\t')
                content = (list(row) for row in df.values)
            elif parser_type == 'csv':
                content = self._parse_csv(lexique_path)
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

    def _create_db(self, lexicon: Generator[list, Any, None]) -> None:  #type: ignore[type-arg]
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
            sorted_form = ''.join(sorted(lexical_entry.ortho))
            self.anagrams[sorted_form].append(lexical_entry)
            if converted_row_fields[0] in self.lexique and not isinstance(self.lexique[converted_row_fields[0]], list):
                self.lexique[converted_row_fields[0]] = [self.lexique[converted_row_fields[0]]]
                self.lexique[converted_row_fields[0]].append(lexical_entry)
            elif converted_row_fields[0] in self.lexique and isinstance(self.lexique[converted_row_fields[0]], list):
                self.lexique[converted_row_fields[0]].append(lexical_entry)
            else:
                self.lexique[converted_row_fields[0]] = lexical_entry
        return

    def _convert_entries(self, row_fields: Union[List[str], List[Union[str, float, int, bool]]]) -> ConvertedRow:
        """
        | Convert entries from `strings` to `int`, `bool` or `float` and generates
        | a new list with typed entries.

        :param row_fields:
            List of column entries representing a row.
        :return: ConvertedRow:
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
        return converted_row_fields  # type: ignore[return-value]

    def get_lex(self, words: Union[Tuple[str, ...], str]) -> Dict[str, Union[LexItem, List[LexItem]]]:
        """
        Recovers the lexical entries for the words in the sequence

        :param words:
            A string or a tuple of multiple strings for getting the LexItems for multiple words.
        :return:
            Dictionary of LexItems.
        :raises: TypeError.
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
        :raises: ValueError.
        :raises: TypeError.
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
            distinct = {elmt.lemme for elmt in lex_entry}
            lemmes = []
            for lemme in distinct:
                lemmes.extend(self.lemmes[lemme])
        else:
            raise TypeError
        return lemmes

    def get_anagrams(self, word: str) -> List[LexItem]:
        """
        Gets all lexical forms of a given word.

        :param word:
            String.
        :return:
            List of LexItem objects which are anagrams of the given word.
        :raises: ValueError.
        :raises: TypeError.
        """
        try:
            lex_entry = self.lexique[word.lower()]
        except ValueError as e:
            logger.warning('The word {} is not in Lexique383\n'.format(word))
            raise ValueError from e
        if isinstance(lex_entry, LexItem):
            sorted_form = ''.join(sorted(lex_entry.ortho))
            anagrams = self.anagrams[sorted_form]
        elif isinstance(lex_entry, OrderedDict):
            sorted_form = ''.join(sorted(lex_entry['ortho']))
            anagrams = self.anagrams[sorted_form]
        elif isinstance(lex_entry, list):
            sorted_form = ''.join(sorted(lex_entry[0].ortho))
            anagrams = self.anagrams[sorted_form]
        else:
            raise TypeError
        final_anagrams = [lex_item for lex_item in anagrams if lex_item.ortho != word.lower()]
        return final_anagrams

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
