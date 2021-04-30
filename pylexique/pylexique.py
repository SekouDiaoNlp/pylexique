# -*- coding: utf-8 -*-

"""Main module of pylexique."""

from collections import OrderedDict, defaultdict
import pkg_resources

from dataclasses import asdict, dataclass, astuple
from typing import ClassVar
from time import time

_RESOURCE_PACKAGE = __name__

PYLEXIQUE_DATABASE = '/'.join(('Lexique383', 'lexique383.xlsb'))
HOME_PATH = '/'.join(('Lexique', ''))
PICKLE_PATH = '/'.join(('Lexique383', 'lexique383.zip'))
_RESOURCE_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'Lexique383/Lexique383.txt')

LEXIQUE383_FIELD_NAMES = ['ortho', 'phon', 'lemme', 'cgram', 'genre', 'nombre', 'freqlemfilms2', 'freqlemlivres',
                          'freqfilms2',
                          'freqlivres', 'infover', 'nbhomogr', 'nbhomoph', 'islem', 'nblettres', 'nbphons', 'cvcv',
                          'p_cvcv',
                          'voisorth', 'voisphon', 'puorth', 'puphon', 'syll', 'nbsyll', 'cv_cv', 'orthrenv', 'phonrenv',
                          'orthosyll', 'cgramortho', 'deflem', 'defobs', 'old20', 'pld20', 'morphoder', 'nbmorph']


class LexEntryTypes:
    """
    Hint type information.

    """
    ortho = str
    phon = str
    lemme = str
    cgram = str
    genre = str
    nombre = str
    freqlemfilms2 = float
    freqlemlivres = float
    freqfilms2 = float
    freqlivres = float
    infover = str
    nbhomogr = int
    nbhomoph = int
    islem = bool
    nblettres = int
    nbphons = int
    cvcv = str
    p_cvcv = str
    voisorth = int
    voisphon = int
    puorth = int
    puphon = int
    syll = str
    nbsyll = int
    cv_cv = str
    orthrenv = str
    phonrenv = str
    orthosyll = str
    cgramortho = str
    deflem = float
    defobs = int
    old20 = float
    pld20 = float
    morphoder = str
    nbmorph = int
    id = int


class Lexique383:
    """
    This is the class handling the lexique database.
    It provides method for interacting with the Lexique DB
    and retrieve lexical items.
    All the lexical items are then stored in an Ordered Dict called

    :param lexique_path: string.
        Path to the lexique csv file.
    """

    file_name = pkg_resources.resource_filename(_RESOURCE_PACKAGE, PYLEXIQUE_DATABASE)

    def __init__(self, lexique_path=None):
        self.lexique_path = lexique_path
        self.lexique = OrderedDict()
        if lexique_path:
            t0 = time()
            self._parse_lexique(self.lexique_path)
            t1 = round(time() - t0, 2)
        else:
            try:
                # Tries to load the pre-shipped Lexique38X if no path file to the lexicon is provided.
                self._parse_lexique(_RESOURCE_PATH)
            except FileNotFoundError:
                if isinstance(lexique_path, str):
                    raise ValueError(f"Argument 'lexique_path' must be a valid path to Lexique383")
                if not isinstance(lexique_path, str):
                    raise TypeError(f"Argument 'lexique_path'must be of type String, not {type(lexique_path)}")
        return

    def __repr__(self):
        return '{0}.{1}'.format(__name__, self.__class__.__name__)

    def __len__(self):
        return len(self.lexique)

    def _parse_lexique(self, lexique_path):
        """
        | Parses the given lexique file and creates a hdf5 table to store the data.

        :param lexique_path: string.
            Path to the lexique csv file.
        :return:
        """
        with open(lexique_path, 'r', encoding='utf-8', errors='ignore') as csv_file:
            content = csv_file.readlines()
            self._create_db(content)
        return

    def _create_db(self, lexicon):
        """
        | Creates an hdf5 table populated with the entries in lexique if it does not exist yet.
        | It stores the hdf5 database for fast access.

        :param lexicon: Iterable.
            Iterable containing the lexique383 entries.
        :return:
        """
        for i, row in enumerate(lexicon[1:]):
            row_fields = row.strip().split('\t')
            row_fields = self._convert_entries(row_fields)
            if row_fields[0] in self.lexique and not isinstance(self.lexique[row_fields[0]], list):
                self.lexique[row_fields[0]] = [self.lexique[row_fields[0]]]
                self.lexique[row_fields[0]].append(LexItem(row_fields))
            elif row_fields[0] in self.lexique and isinstance(self.lexique[row_fields[0]], list):
                self.lexique[row_fields[0]].append(LexItem(row_fields))
            else:
                self.lexique[row_fields[0]] = LexItem(row_fields)
        return

    @staticmethod
    def _convert_entries(row_fields):
        """
        | Convert entries from `strings` to `int` or `float` and generates
        | a new list with typed entries.

        :param row_fields:
        :return: converted_row_fields:
        """
        errors = defaultdict(list)
        converted_row_fields = []
        for attr, value in zip(LEXIQUE383_FIELD_NAMES, row_fields):
            if attr in {'freqlemfilms2', 'freqlemlivres', 'freqfilms2', 'freqlivres', 'old20', 'pld20'}:
                if (value != '' or value != ' ') and ',' in value:
                    value = value.replace(',', '.')
                    value = float(value)
            if attr in {'nbhomogr', 'nbhomoph', 'islem', 'nblettres', 'nbphons', 'voisorth', 'voisphon', 'puorth',
                        'puphon', 'nbsyll'}:
                if value != '' or value != ' ':
                    try:
                        value = int(value)
                    except ValueError:
                        print(
                            "the value {} is of the wrong type for the attribute '{}'. Keeping value as string.\n".format(
                                value, attr))
                        errors[row_fields[0]].append({attr: value})
                        value = value
            converted_row_fields.append(value)
        row_fields = converted_row_fields
        return row_fields


@dataclass(init=False, repr=False, eq=True, order=False, unsafe_hash=False, frozen=False)
class LexItem:
    """
    | This class defines the lexical items in Lexique383.
    | It uses slots for memory efficiency.

    :param row_fields:
    """
    _s: ClassVar[list] = LEXIQUE383_FIELD_NAMES + ['_name_']
    __slots__ = _s
    _name_: str
    for attr in LEXIQUE383_FIELD_NAMES:
        attr: LexEntryTypes

    def __init__(self, row_fields):
        fields = row_fields
        setattr(self, '_name_', fields[0])
        for attr, value in zip(LEXIQUE383_FIELD_NAMES, fields):
            if attr != 'attr':
                setattr(self, attr, value)
        return

    def __repr__(self):
        return '{0}.{1}({2}, {3}, {4})'.format(__name__, self.__class__.__name__, self.ortho, self.lemme, self.cgram)

    def to_dict(self):
        """
        | Converts the LexItem to a dict containing its attributes and their values

        :return: dict
        """
        attributes = []
        for attr in self.__slots__:
            if not attr == "_name_":
                try:
                    value = getattr(self, attr)
                except AttributeError as e:
                    print(e)
                    pass
                attributes.append((attr, value))
        result = OrderedDict(attributes)
        # result = OrderedDict((attr, getattr(self, attr)) for attr in self.__slots__ if attr != 'attr')
        return result


if __name__ == "__main__":
    pass
