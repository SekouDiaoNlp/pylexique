"""Main module of pylexique."""

from collections import OrderedDict, defaultdict
from collections.abc import Sequence
from enum import Enum
import pkg_resources
import sqlite3
import json
from math import isnan
# import faster_than_csv as csv
import csv
from dataclasses import dataclass
from typing import DefaultDict, Dict, List, Optional, Tuple, Union, Generator, Any, Iterator

__all__ = ['Lexique383', 'LexItem', 'LexEntryTypes']

try:
    from utils import logger
except (ModuleNotFoundError, ImportError):
    from .utils import logger

_RESOURCE_PACKAGE = __name__

HOME_PATH = '/'.join(('Lexique', ''))
_RESOURCE_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'Lexique383/Lexique383.db')
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


class Genre(Enum):
    MASCULIN = 'm'
    FEMININ = 'f'


class Nombre(Enum):
    SINGULIER = 's'
    PLURIEL = 'p'


@dataclass(init=True, repr=False, eq=True, order=False, unsafe_hash=False)
class LexEntryTypes:
    ortho: str
    phon: str
    lemme: str
    cgram: str
    genre: Genre  # Use the Genre enum
    nombre: Nombre  # Use the Nombre enum
    freqlemfilms2: float
    freqlemlivres: float
    freqfilms2: float
    freqlivres: float
    infover: str
    nbhomogr: int
    nbhomoph: int
    islem: int  # Use int for boolean attribute
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
    defobs: int  # Use int for boolean attribute
    old20: float
    pld20: float
    morphoder: str
    nbmorph: int


@dataclass(init=True, repr=False, eq=True, order=False, unsafe_hash=False)
class LexItem(LexEntryTypes):
    _s = LEXIQUE383_FIELD_NAMES
    __slots__ = _s

    def __repr__(self) -> str:
        return '{0}({1}, {2}, {3})'.format(self.__class__.__name__, self.ortho, self.lemme, self.cgram)

    def to_dict(self) -> Dict[str, Union[str, float, int]]:
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
    def __init__(self, lexique_path: str = _RESOURCE_PATH) -> None:
        self.lexique_path = lexique_path
        self.db_conn = sqlite3.connect(lexique_path)
        self.db_cursor = self.db_conn.cursor()

    def __repr__(self) -> str:
        return '{0}.{1}'.format(__name__, self.__class__.__name__)

    def __del__(self) -> None:
        self.db_conn.close()

    def get_lex(self, words: Union[Tuple[str, ...], str]) -> Dict[str, Union[LexItem, List[LexItem]]]:
        results = {}

        if isinstance(words, str):
            results[words] = self._fetch_lex_items_by_ortho(words.lower())
        elif isinstance(words, Sequence):
            for word in words:
                if isinstance(word, str):
                    results[word] = self._fetch_lex_items_by_ortho(word.lower())
                else:
                    logger.warning('{} is not a valid string'.format(word))
                    raise TypeError
        else:
            raise TypeError

        return results

    def get_all_forms(self, word: str) -> Union[LexItem, List[LexItem]]:
        return self._fetch_lex_items_by_lemme(word.lower())

    def get_anagrams(self, word: str) -> Union[LexItem, List[LexItem]]:
        return self._fetch_anagrams(word.lower())

    def _fetch_lex_items_by_ortho(self, ortho: str) -> Union[LexItem, List[LexItem]]:
        query = "SELECT * FROM lexique WHERE ortho = ?"
        self.db_cursor.execute(query, (ortho,))
        rows = self.db_cursor.fetchall()
        return self._create_lex_items(rows)

    def _fetch_lex_items_by_lemme(self, lemme: str) -> Union[LexItem, List[LexItem]]:
        lemmes_query = "SELECT lemme FROM lexique WHERE ortho = ?"
        self.db_cursor.execute(lemmes_query, (lemme,))
        lemmes = self.db_cursor.fetchall()
    
        if not lemmes:
            return []
    
        lemmes = [row[0] for row in lemmes]
    
        query = "SELECT * FROM lexique WHERE lemme IN ({})".format(', '.join('?' for _ in lemmes))
        self.db_cursor.execute(query, lemmes)
        rows = self.db_cursor.fetchall()
        return self._create_lex_items(rows)

    def _fetch_anagrams(self, ortho: str) -> Union[LexItem, List[LexItem]]:
        sorted_ortho = ''.join(sorted(ortho))
        query = "SELECT * FROM lexique WHERE sorted_ortho = ?"
        self.db_cursor.execute(query, (sorted_ortho, ))
        rows = self.db_cursor.fetchall()
        return self._create_lex_items(rows)

    def _create_lex_items(self, rows: List[Tuple]) -> Union[LexItem, List[LexItem]]: # type: ignore[type-arg]
        if len(rows) == 0:
            return []
        elif len(rows) == 1:
            return LexItem(*rows[0][:-1])
        else:
            return [LexItem(*row[:-1]) for row in rows]


if __name__ == "__main__":
    pass
