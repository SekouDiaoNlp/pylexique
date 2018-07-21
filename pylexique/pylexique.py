# -*- coding: utf-8 -*-

"""Main module."""

from collections import OrderedDict, defaultdict
import pickle
import pkg_resources


_RESOURCE_PACKAGE = __name__

LEXIQUE382_PATH = '/'.join(('Lexique382', 'lexique382.pickle'))

LEXIQUE382_FIELD_NAMES = ['ortho', 'phon', 'lemme', 'cgram', 'genre', 'nombre', 'freqlemfilms2', 'freqlemlivres', 'freqfilms2',
                          'freqlivres', 'infover', 'nbhomogr', 'nbhomoph', 'islem', 'nblettres', 'nbphons', 'cvcv', 'p_cvcv',
                          'voisorth', 'voisphon', 'puorth', 'puphon', 'syll', 'nbsyll', 'cv_cv', 'orthrenv', 'phonrenv',
                          'orthosyll', 'cgramortho', 'deflem', 'defobs', 'old20', 'pld20', 'morphoder', 'nbmorph']


class Lexique382(object):
    """

    :param lexique:
    """

    def __init__(self, lexique_path=None):
        self.lexique_path = lexique_path
        self.lexique = OrderedDict
        if lexique_path:
            self.lexique = self.parse_lexique(self.lexique_path)
        else:
            file_path = pkg_resources.resource_filename(_RESOURCE_PACKAGE, LEXIQUE382_PATH)
            with open(file_path, 'rb') as file:
                self.lexique = pickle.load(file)


    def __repr__(self):
        return '{0}.{1}'.format(__name__, self.__class__.__name__)

    def __len__(self):
        return len(self.lexique)

    # def __iter__(self):
    #     return self
    #
    # def __next__(self):
    #     self.__idx__ += 1
    #     try:
    #         return self.lexique[self.__idx__ - 1]
    #     except IndexError:
    #         self.__idx__ = 0
    #         raise StopIteration
    #
    # def __reversed__(self):
    #     return reversed(self.lexique)
    #
    # next = __next__  # Python 2.7 compatibility for iterator protocol

    def parse_lexique(self, lexique_path):
        """

        :param lexique_path:
        :return:
        """
        with open(lexique_path, 'r', encoding='utf-8') as csv_file:
            content = csv_file.readlines()
            fields = [field.split('_')[-1] for field in content[0].strip().split('\t')]
            if fields[17] == 'cvcv':
                fields[17] = 'p_cvcv'
            if fields[24] == 'cv-cv':
                fields[17] = 'cv_cv'
            lexique382_dict = defaultdict(list)
            for row in content[1:]:
                row_fields = row.strip().split('\t')
                lexique382_dict[row_fields[0]].append(LexEntry(row_fields))
                pass
            return lexique382_dict


class LexEntry(object):
    """

    :param row_fields:
    """
    __slots__ = LEXIQUE382_FIELD_NAMES

    def __init__(self, row_fields):
        for attr, value in zip(LEXIQUE382_FIELD_NAMES, row_fields):
            setattr(self, attr, value)

    def __repr__(self):
        return '{0}.{1}({2}, {3}, {4})'.format(__name__, self.__class__.__name__, self.ortho, self.lemme, self.cgram)

    pass


if __name__ == "__main__":
    # test = Lexique382('C:/Users/Utilisateur/PycharmProjects/pylexique/pylexique/Lexique382/Lexique382.txt')
    test1 = Lexique382()
    print('ok')
    pass
