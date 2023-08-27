from collections import OrderedDict
from dataclasses import dataclass
from enum import Enum
import json
from math import isnan
import pkg_resources
from sqlalchemy import create_engine, Column, Integer, Float, String, Enum as SAEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import class_mapper
from typing import DefaultDict, Dict, List, Optional, Tuple, Union

__all__ = ['Lexique383', 'LexItem', 'LexEntryTypes']

try:
    from utils import logger
except (ModuleNotFoundError, ImportError):
    from .utils import logger					

_RESOURCE_PACKAGE = __name__

HOME_PATH = '/'.join(('Lexique', ''))
RESOURCE_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'Lexique383/Lexique383_id.db')

LEXIQUE383_FIELD_NAMES = ['ortho', 'phon', 'lemme', 'cgram', 'genre', 'nombre', 'freqlemfilms2', 'freqlemlivres',
                          'freqfilms2',
                          'freqlivres', 'infover', 'nbhomogr', 'nbhomoph', 'islem', 'nblettres', 'nbphons', 'cvcv',
                          'p_cvcv',
                          'voisorth', 'voisphon', 'puorth', 'puphon', 'syll', 'nbsyll', 'cv_cv', 'orthrenv', 'phonrenv',
                          'orthosyll', 'cgramortho', 'deflem', 'defobs', 'old20', 'pld20', 'morphoder', 'nbmorph', 'sorted_ortho']

ConvertedRow = Tuple[str, str, str, str, str, str, float, float, float, float, str, int, int, bool,
                     int, int, str, str, int, int, int, int, str, int, str, str, str, str, str, float,
                     int, float, float, str, int, str]

Base = declarative_base()

class LexEntryTypes(Base):
    __tablename__ = 'lexique'
    mapper_args__ = {
        "exclude_properties": [id],  # Exclude id column from queries
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    ortho = Column(String)
    phon = Column(String)
    lemme = Column(String)
    cgram = Column(String)
    genre = Column(String)
    nombre = Column(String)
    freqlemfilms2 = Column(Float)
    freqlemlivres = Column(Float)
    freqfilms2 = Column(Float)
    freqlivres = Column(Float)
    infover = Column(String)
    nbhomogr = Column(Integer)
    nbhomoph = Column(Integer)
    islem = Column(Integer)
    nblettres = Column(Integer)
    nbphons = Column(Integer)
    cvcv = Column(String)
    p_cvcv = Column(String)
    voisorth = Column(Integer)
    voisphon = Column(Integer)
    puorth = Column(Integer)
    puphon = Column(Integer)
    syll = Column(String)
    nbsyll = Column(Integer)
    cv_cv = Column(String)
    orthrenv = Column(String)
    phonrenv = Column(String)
    orthosyll = Column(String)
    cgramortho = Column(String)
    deflem = Column(Float)
    defobs = Column(Integer)
    old20 = Column(Float)
    pld20 = Column(Float)
    morphoder = Column(String)
    nbmorph = Column(Integer)
    sorted_ortho = Column(String)


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
    
    @classmethod
    def from_orm(cls, row):
        instance = cls()
        for column in class_mapper(cls).mapped_table.columns:
            setattr(instance, column.name, getattr(row, column.name))
        return instance


class Lexique383:
    def __init__(self, lexique_path: str = RESOURCE_PATH):
        self.engine = create_engine(f'sqlite:///{lexique_path}')
        self.Session = sessionmaker(bind=self.engine)

    def __del__(self):
        self.engine.dispose()

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
        with self.Session() as session:
            rows = session.query(LexEntryTypes).filter_by(ortho=ortho).all()
        return self._create_lex_items(rows)

    def _fetch_lex_items_by_lemme(self, lemme: str) -> Union[LexItem, List[LexItem]]:
        with self.Session() as session:
            lemmes = session.query(LexEntryTypes.lemme).filter_by(ortho=lemme).all()
            lemmes = [row[0] for row in lemmes]
            rows = session.query(LexEntryTypes).filter(LexEntryTypes.lemme.in_(lemmes)).all()
        return self._create_lex_items(rows)

    def _fetch_anagrams(self, ortho: str) -> Union[LexItem, List[LexItem]]:
        sorted_ortho = ''.join(sorted(ortho))
        with self.Session() as session:
            rows = session.query(LexEntryTypes).filter_by(sorted_ortho=sorted_ortho).all()
        return self._create_lex_items(rows)

    def _create_lex_items(self, rows) -> Union[LexItem, List[LexItem]]:
        if len(rows) == 0:
            return []
        elif len(rows) == 1:
            return LexItem.from_orm(rows[0])
        else:
            return [LexItem.from_orm(row) for row in rows]

if __name__ == "__main__":
    pass
