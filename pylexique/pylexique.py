# -*- coding: utf-8 -*-

"""Main module of pylexique."""

from collections import OrderedDict
import pkg_resources
import json
import joblib
from zipfile import ZipFile
import atexit
from dataclasses import dataclass
from typing import ClassVar

_RESOURCE_PACKAGE = __name__

PYLEXIQUE_DATABASE = '/'.join(('Lexique383', 'lexique383.xlsb'))
HOME_PATH = '/'.join(('Lexique', ''))

LEXIQUE383_FIELD_NAMES = ['ortho', 'phon', 'lemme', 'cgram', 'genre', 'nombre', 'freqlemfilms2', 'freqlemlivres',
                          'freqfilms2',
                          'freqlivres', 'infover', 'nbhomogr', 'nbhomoph', 'islem', 'nblettres', 'nbphons', 'cvcv',
                          'p_cvcv',
                          'voisorth', 'voisphon', 'puorth', 'puphon', 'syll', 'nbsyll', 'cv_cv', 'orthrenv', 'phonrenv',
                          'orthosyll', 'cgramortho', 'deflem', 'defobs', 'old20', 'pld20', 'morphoder', 'nbmorph']


LEXIQUE = OrderedDict()


# class LexEntry(tables.IsDescription):
#     """
#     Schema for the Lexique383 database table in HDF5 format.
#
#     """
#     ortho = tables.StringCol(64)
#     phon = tables.StringCol(64)
#     lemme = tables.StringCol(64)
#     cgram = tables.StringCol(32)
#     genre = tables.StringCol(8)
#     nombre = tables.StringCol(8)
#     freqlemfilms2 = tables.Float32Col()
#     freqlemlivres = tables.Float32Col()
#     freqfilms2 = tables.Float32Col()
#     freqlivres = tables.Float32Col()
#     infover = tables.StringCol(32)
#     nbhomogr = tables.Int8Col()
#     nbhomoph = tables.Int8Col()
#     islem = tables.BoolCol()
#     nblettres = tables.Int8Col()
#     nbphons = tables.Int8Col()
#     cvcv = tables.StringCol(64)
#     p_cvcv = tables.StringCol(64)
#     voisorth = tables.Int8Col()
#     voisphon = tables.Int8Col()
#     puorth = tables.Int8Col()
#     puphon = tables.Int8Col()
#     syll = tables.StringCol(64)
#     nbsyll = tables.Int8Col()
#     cv_cv = tables.StringCol(64)
#     orthrenv = tables.StringCol(64)
#     phonrenv = tables.StringCol(64)
#     orthosyll = tables.StringCol(64)
#     cgramortho = tables.StringCol(32)
#     deflem = tables.Float32Col()
#     defobs = tables.Int8Col()
#     old20 = tables.Float32Col()
#     pld20 = tables.Float32Col()
#     morphoder = tables.StringCol(64)
#     nbmorph = tables.Int8Col()

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
            print('parsing Lexique383')
            self.parse_lexique(self.lexique_path)
            with ZipFile(pkg_resources.resource_stream(
                    _RESOURCE_PACKAGE, PYLEXIQUE_DATABASE)) as content:
                with content.open('Lexique383.pickle', 'wb') as archive:
                    joblib.dump(self.lexique , archive)
        else:
            self.parse_lexique(self.lexique_path)
            with ZipFile(pkg_resources.resource_stream(
                    _RESOURCE_PACKAGE, PYLEXIQUE_DATABASE)) as content:
                with content.open('Lexique383.pickle', 'rb') as archive:
                    joblib.load(archive)
        print('Lexique 383 loaded successfully')
        return

    def __repr__(self):
        return '{0}.{1}'.format(__name__, self.__class__.__name__)

    def __len__(self):
        return len(self.lexique)

    def parse_lexique(self, lexique_path):
        """
        | Parses the given lexique file and creates a hdf5 table to store the data.

        :param lexique_path: string.
            Path to the lexique csv file.
        :return: PyTables.Table
        """
        with open(lexique_path, 'r', encoding='utf-8', errors='ignore') as csv_file:
            content = csv_file.readlines()
            lexique383_db = (content[1:])
            self.create_db(lexique383_db)
        return

    def create_db(self, lexicon):
        """
        | Creates an hdf5 table populated with the entries in lexique if it does not exist yet.
        | It stores the hdf5 database for fast access.

        :param lexicon: Iterable.
            Iterable containing the lexique383 entries.
        :return: PyTables.Table
        """
        errors = {}
        for i, row in enumerate(lexicon):
            row_fields = row.strip().split('\t')
            for field, value in zip(LEXIQUE383_FIELD_NAMES, row_fields):
                if getattr(LexEntryTypes, field) == float:
                    value = value.replace(',', '.')
                try:
                    formatted_value = getattr(LexEntryTypes, field)(value)
                except ValueError:
                    errors[value] = field
                    formatted_value = value
                finally:
                    self.lexique[row_fields[0]] = formatted_value
        return


# class Lexique383_b:
#     """
#     This is the class handling the lexique database.
#     It provides method for interacting with the Lexique DB
#     and retrieve lexical items.
#     All the lexical items are then stored in an Ordered Dict called
#
#     :param lexique_path: string.
#         Path to the lexique csv file.
#     """
#
#     file_name = pkg_resources.resource_filename(_RESOURCE_PACKAGE, PYLEXIQUE_DATABASE)
#
#     def __init__(self, lexique_path=None):
#         self.lexique_path = lexique_path
#         self.lexique = OrderedDict
#         if lexique_path:
#             self.lexique = self.parse_lexique(self.lexique_path)
#         else:
#             h5file = tables.open_file(__class__.file_name, mode="r", title="pylexique")
#             self.lexique = h5file.root.lexique383.data
#         return
#
#     def __repr__(self):
#         return '{0}.{1}'.format(__name__, self.__class__.__name__)
#
#     def __len__(self):
#         return len(self.lexique)
#
#     def parse_lexique(self, lexique_path):
#         """
#         | Parses the given lexique file and creates a hdf5 table to store the data.
#
#         :param lexique_path: string.
#             Path to the lexique csv file.
#         :return: PyTables.Table
#         """
#         with open(lexique_path, 'r', encoding='utf-8', errors='ignore') as csv_file:
#             content = csv_file.readlines()
#             lexique383_db = self.create_table(content[1:])
#         return lexique383_db
#
#     def create_table(self, lexique):
#         """
#         | Creates an hdf5 table populated with the entries in lexique if it does not exist yet.
#         | It stores the hdf5 database for fast access.
#
#         :param lexique: Iterable.
#             Iterable containing the lexique383 entries.
#         :return: PyTables.Table
#         """
#         filters = tables.Filters(complib='zlib', complevel=5)
#         h5file = tables.open_file(self.file_name, mode="w", title="pylexique", filters=filters)
#         group = h5file.create_group("/", 'lexique383', 'Lexique383')
#         table = h5file.create_table(group, 'data', LexEntry, "Lexique383 Database")
#         lex_row = table.row
#         errors = {}
#         for i, row in enumerate(lexique):
#             row_fields = row.strip().split('\t')
#             for field, value in zip(LEXIQUE383_FIELD_NAMES, row_fields):
#                 if field in ('freqlemfilms2', 'freqlemlivres', 'freqfilms2', 'freqlivres', 'deflem', 'old20', 'pld20'):
#                     if value == '':
#                         value = 'nan'
#                     lex_row[field] = float(value.replace(',', '.'))
#                 elif field in ('nbhomogr', 'nbhomoph', 'nblettres', 'nbphons', 'voisorth', 'voisphon',
#                                'puorth', 'puphon', 'nbsyll', 'defobs', 'nbmorph'):
#                     if value == '':
#                         value = '0'
#                     try:
#                         lex_row[field] = int(value)
#                     except ValueError:
#                         print(
#                             'There was an error  at row {3} in the world {0} with the field {1} having value {2}.\n'.
#                             format(row_fields[0], field, value, i + 1))
#                         errors[i + 1] = row_fields
#                         continue
#                 elif field in ('cgram', 'cgramortho', 'ortho', 'phon', 'orthosyll', 'syll', 'orthrenv', 'phonrenv', 'lemme', 'morphoder'):
#                     lex_row[field] = value.encode('utf-8')
#                 else:
#                     lex_row[field] = value.encode('utf-8')
#                 lex_info = LexItem(row)
#                 LEXIQUE[lex_info.ortho] = lex_info
#             lex_row.append()
#         json.dumps(errors, indent=4)
#         return table, LEXIQUE


@dataclass(init=False, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)
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
        fields = row_fields.strip().split('\t')
        setattr(self, '_name_', fields[0])
        for attr, value in zip(LEXIQUE383_FIELD_NAMES, fields):
            setattr(self, attr, value)
        return


if __name__ == "__main__":
    pass
