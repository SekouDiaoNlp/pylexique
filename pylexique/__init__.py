# -*- coding: utf-8 -*-

"""Top-level package for pylexique."""

__author__ = """SekouDiaoNlp"""
__email__ = 'diao.sekou.nlp@gmail.com'
__version__ = '1.0.7'
__copyright__ = "Copyright (c) 2021, SekouDiaoNlp"
__credits__ = ("Lexique383",)
__license__ = "MIT"
__maintainer__ = "SekouDiaoNlp"
__status__ = "Production"

from collections import OrderedDict
import pkg_resources
import tables
import json
import atexit
from .utils import my_close_open_files
from .pylexique import Lexique383

# PYLEXIQUE_DATABASE = '/'.join(('Lexique383', 'lexique383.h5'))
# HOME_PATH = '/'.join(('Lexique', ''))

lexique383, LEXIQUE = Lexique383('Lexique383/Lexique383.txt')
# lexique383, LEXIQUE = Lexique383()  # Use only if the hdf5 file exists.

print('Lexique8 has been successfully loaded.\n')
