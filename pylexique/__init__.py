# -*- coding: utf-8 -*-

"""Top-level package for pylexique."""

__author__ = """SekouDiaoNlp"""
__email__ = 'diao.sekou.nlp@gmail.com'
__version__ = '1.1.0'
__copyright__ = "Copyright (c) 2021, SekouDiaoNlp"
__credits__ = ("Lexique383",)
__license__ = "MIT"
__maintainer__ = "SekouDiaoNlp"
__status__ = "Production"

from collections import OrderedDict
import pkg_resources
import json
import pkg_resources
from .utils import my_close_open_files
from .pylexique import Lexique383

# PYLEXIQUE_DATABASE = '/'.join(('Lexique383', 'lexique383.h5'))
# HOME_PATH = '/'.join(('Lexique', ''))

_RESOURCE_PACKAGE = 'pylexique'
_RESOURCE_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'Lexique383/Lexique383.txt')

LEXIQUE = Lexique383(_RESOURCE_PATH).lexique
# lexique383, LEXIQUE = Lexique383()  # Use only if the hdf5 file exists.

print('Lexique8 has been successfully loaded.\n')
