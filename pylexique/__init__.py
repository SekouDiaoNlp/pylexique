# -*- coding: utf-8 -*-

"""Top-level package for pylexique."""

__author__ = """SekouDiaoNlp"""
__email__ = 'diao.sekou.nlp@gmail.com'
__version__ = '1.0.7'

from pylexique.pylexique import Lexique383


lexique383, LEXIQUE = Lexique383('Lexique383/Lexique383.xlsb')
# lexique383, LEXIQUE = Lexique383()  # Use only if the hdf5 file exists.
