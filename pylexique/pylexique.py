# -*- coding: utf-8 -*-

"""Main module."""

from collections import OrderedDict
import pkg_resources
import tables


_RESOURCE_PACKAGE = __name__

LEXIQUE382_PATH = '/'.join(('Lexique382', 'lexique382.pickle'))
PYLEXIQUE_DATABASE = '/'.join(('Lexique382', 'lexique382.h5'))

LEXIQUE382_FIELD_NAMES = ['ortho', 'phon', 'lemme', 'cgram', 'genre', 'nombre', 'freqlemfilms2', 'freqlemlivres', 'freqfilms2',
                          'freqlivres', 'infover', 'nbhomogr', 'nbhomoph', 'islem', 'nblettres', 'nbphons', 'cvcv', 'p_cvcv',
                          'voisorth', 'voisphon', 'puorth', 'puphon', 'syll', 'nbsyll', 'cv_cv', 'orthrenv', 'phonrenv',
                          'orthosyll', 'cgramortho', 'deflem', 'defobs', 'old20', 'pld20', 'morphoder', 'nbmorph']


class LexEntry(tables.IsDescription):
    """
    Schema for the Lexique382 database table.

    """
    ortho = tables.StringCol(64)
    phon = tables.StringCol(64)
    lemme = tables.StringCol(64)
    cgram = tables.StringCol(32)
    genre = tables.StringCol(8)
    nombre = tables.StringCol(8)
    freqlemfilms2 = tables.Float32Col()
    freqlemlivres = tables.Float32Col()
    freqfilms2 = tables.Float32Col()
    freqlivres = tables.Float32Col()
    infover = tables.StringCol(32)
    nbhomogr = tables.Int8Col()
    nbhomoph = tables.Int8Col()
    islem = tables.BoolCol()
    nblettres = tables.Int8Col()
    nbphons = tables.Int8Col()
    cvcv = tables.StringCol(64)
    p_cvcv = tables.StringCol(64)
    voisorth = tables.Int8Col()
    voisphon = tables.Int8Col()
    puorth = tables.Int8Col()
    puphon = tables.Int8Col()
    syll = tables.StringCol(64)
    nbsyll = tables.Int8Col()
    cv_cv = tables.StringCol(64)
    orthrenv = tables.StringCol(64)
    phonrenv = tables.StringCol(64)
    orthosyll = tables.StringCol(64)
    cgramortho = tables.StringCol(32)
    deflem = tables.Float32Col()
    defobs = tables.Int8Col()
    old20 = tables.Float32Col()
    pld20 = tables.Float32Col()
    morphoder = tables.StringCol(64)
    nbmorph = tables.Int8Col()


class Lexique382(object):
    """
    This is the class handling the lexique database.

    :param lexique_path: string.
        Path to the lexuique csv file.
    """

    def __init__(self, lexique_path=None):
        self.lexique_path = lexique_path
        self.lexique = OrderedDict
        if lexique_path:
            self.lexique = self.parse_lexique(self.lexique_path)
        else:
            file_name = pkg_resources.resource_filename(_RESOURCE_PACKAGE, PYLEXIQUE_DATABASE)
            h5file = tables.open_file(file_name, mode="r", title="pylexique")
            self.lexique = h5file.root.lexique382.data
            # file_path = pkg_resources.resource_filename(_RESOURCE_PACKAGE, LEXIQUE382_PATH)
            # with open(file_path, 'rb') as file:
            #     self.lexique = pickle.load(file)
        return

    def __repr__(self):
        return '{0}.{1}'.format(__name__, self.__class__.__name__)

    def __len__(self):
        return len(self.lexique)

    def parse_lexique(self, lexique_path):
        """
        Parses the given lexique csv file and creates a hdf5 table to store the data.

        :param lexique_path: string.
            Path to the lexuique csv file.
        :return: PyTables.Table
        """
        with open(lexique_path, 'r', encoding='utf-8') as csv_file:
            content = csv_file.readlines()
            fields = [field.split('_')[-1] for field in content[0].strip().split('\t')]
            if fields[17] == 'cvcv':
                fields[17] = 'p_cvcv'
            if fields[24] == 'cv-cv':
                fields[17] = 'cv_cv'
            lexique382_db = self.create_table(content[1:])
        return lexique382_db

    def create_table(self, lexique):
        """
        Creates an hdf5 table populated with the entries in lexique.

        :param lexique: Iterable.
            Iterable containing the lexique382 entries.
        :return: PyTables.Table
        """
        file_name = pkg_resources.resource_filename(_RESOURCE_PACKAGE, PYLEXIQUE_DATABASE)
        h5file = tables.open_file(file_name, mode="w", title="pylexique")
        group = h5file.create_group("/", 'lexique382', 'Lexique382')
        table = h5file.create_table(group, 'data', LexEntry, "Lexique382 Database")
        lex_item = table.row
        for row in lexique:
            row_fields = row.strip().split('\t')
            for field, value in zip(LEXIQUE382_FIELD_NAMES, row_fields):
                if field in ('freqlemfilms2', 'freqlemlivres', 'freqfilms2', 'freqlivres', 'deflem', 'old20', 'pld20'):
                    if value == '':
                        value = 'nan'
                    lex_item[field] = float(value)
                elif field in ('nbhomogr', 'nbhomoph', 'nblettres', 'nbphons', 'voisorth', 'voisphon',
                               'puorth', 'puphon', 'nbsyll', 'defobs', 'nbmorph'):
                    if value == '':
                        value = '0'
                    lex_item[field] = int(value)
                elif field in ('ortho', 'phon', 'orthosyll', 'syll', 'orthrenv', 'phonrenv', 'lemme', 'morphoder'):
                    lex_item[field] = value.encode('utf-8')
                else:
                    lex_item[field] = value
            lex_item.append()
        table.flush()
        return table


class LexItem(object):
    """
    This class defines the lexical items in Lexique382.

    :param row_fields:
    """
    __slots__ = LEXIQUE382_FIELD_NAMES

    def __init__(self, row_fields):
        for attr, value in zip(LEXIQUE382_FIELD_NAMES, row_fields):
            setattr(self, attr, value)
        return

    def __repr__(self):
        return '{0}.{1}({2}, {3}, {4})'.format(__name__, self.__class__.__name__, self.ortho, self.lemme, self.cgram)





if __name__ == "__main__":
    # test = Lexique382('C:/Users/Utilisateur/PycharmProjects/pylexique/pylexique/Lexique382/Lexique382.txt')
    test1 = Lexique382()
    auxes = [x[:] for x in test1.lexique.iterrows() if x['cgram'].decode('utf-8') == 'AUX']
    verbs = [x[:] for x in test1.lexique.iterrows() if x['cgram'].decode('utf-8') == 'VER']
    print('ok')
    pass
