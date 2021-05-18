=========
pylexique
=========


.. image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
        :target: https://GitHub.com/SekouDiaoNlp/pylexique/graphs/commit-activity
        :alt: Package Maintenance Status

.. image:: https://img.shields.io/badge/maintainer-SekouDiaoNlp-blue
        :target: https://GitHub.com/SekouDiaoNlp/pylexique
        :alt: Package Maintener

.. image:: https://img.shields.io/github/checks-status/SekouDiaoNlp/pylexique/master?label=Build%20status%20on%20Windows%2C%20MacOs%20and%20Linux
        :target: https://img.shields.io/github/checks-status/SekouDiaoNlp/pylexique/master
        :alt: Build status on Windows, MacOs and Linux

.. image:: https://img.shields.io/pypi/v/pylexique.svg
        :target: https://pypi.python.org/pypi/pylexique
        :alt: Pypi Python Package Index Status

.. image:: https://anaconda.org/conda-forge/pylexique/badges/version.svg
        :target: https://anaconda.org/conda-forge/pylexique
        :alt: Anaconda Package Index Status

.. image:: https://img.shields.io/pypi/pyversions/pylexique
        :target: https://pypi.python.org/pypi/pylexique
        :alt: Compatible Python versions

.. image:: https://img.shields.io/conda/pn/conda-forge/pylexique?color=dark%20green&label=Supported%20platforms
        :target: https://anaconda.org/conda-forge/pylexique
        :alt: Supported platforms

.. image:: https://readthedocs.org/projects/pylexique/badge/?version=latest
        :target: https://pylexique.readthedocs.io/en/latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/SekouDiaoNlp/pylexique/shield.svg
        :target: https://pyup.io/repos/github/SekouDiaoNlp/pylexique/
        :alt: Dependencies status

.. image:: https://codecov.io/gh/SekouDiaoNlp/pylexique/branch/master/graph/badge.svg?token=EiEXyUJGpF
        :target: https://codecov.io/gh/SekouDiaoNlp/pylexique
        :alt: Code Coverage Status

.. image:: https://snyk-widget.herokuapp.com/badge/pip/pylexique/badge.svg
        :target: https://snyk.io/test/github/SekouDiaoNlp/pylexique?targetFile=requirements.txt
        :alt: Code Vulnerability Status

.. image:: https://img.shields.io/pypi/dm/pylexique?label=PyPi%20Downloads
        :target: https://pypi.org/project/pylexique/
        :alt: PyPI Downloads

.. image:: https://img.shields.io/conda/dn/conda-forge/pylexique?label=Anaconda%20Total%20Downloads
        :target: https://anaconda.org/conda-forge/pylexique
        :alt: Conda


|


| Pylexique is a Python wrapper around Lexique383_.

| It allows to extract lexical information from more than 140 000 French words in an Object Oriented way.

| Each lexical item is represented as a LexItem having the following LexEntryType:
|

.. code-block:: python

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

The meanings of the attributes of this object are as follow:

* ortho: the word
* phon: the phonological forms of the word
* lemme: the lemmas of this word
* cgram: the grammatical categories of this word
* genre: the gender
* nombre: the number
* freqlemfilms: the frequency of the lemma according to the corpus of subtitles (per million occurrences)
* freqlemlivres: the frequency of the lemma according to the body of books (per million occurrences)
* freqfilms: the frequency of the word according to the corpus of subtitles (per million occurrences)
* freqlivres: the frequency of the word according to the body of books (per million occurrences)
* infover: modes, tenses, and possible people for verbs
* nbhomogr: number of homographs
* nbhomoph: number of homophones
* islem: indicates if it is a lemma or not
* nblettres: the number of letters
* nbphons: number of phonemes
* cvcv: the orthographic structure
* p-cvcv: the phonological structure
* voisorth: number of orthographic neighbors
* voisphon: number of phonological neighbors
* puorth: point of spelling uniqueness
* puphon: point of phonological uniqueness
* syll: syllable phonological form
* nbsyll: number of syllables
* cv-cv: syllable phonological structure
* orthrenv: reverse orthographic form
* phonrenv: reversed phonological form
* orthosyll: syllable orthographic form
* cgramortho: the different grammatical category for a given orthographic representation
* deflem: the percentage of people who said they knew the lemma of the word
* defobs: the size of the sample from which 'deflem' is derived
* old20:  orthographic Levenshtein Distance
* pld20: phonological Levenshtein Distance
* morphoder: inflectional morphology
* nbmorph: the number of morphemes directly computed from 'morphoder'


You can find all the relevant information in the `official documentation of Lexique383`_

* Free software: MIT license
* Documentation: https://pylexique.readthedocs.io.


Features
--------

* Extract all lexical information from a French  word such as:
    * orthographic and phonemics representations
    * associated lemmas
    * syllabation
    * grammatical category
    * gender and number
    * frequencies in a corpus of books and in a body of film subtitles, etc...
* Extract all the lexical forms of a French word.
* Easy to use Api.
* Easily integrate pylexique in your own projects as an imported library.
* Can be used as a command line tool.

Credits
-------

Main developer SekouDiaoNlp_.

Lexical corpus: Lexique383_

About Lexique383
================

Lexique3
========

Lexique 3.83 is a French lexical database that provides
for ~ 140,000 words of French: orthographic and phonemics representations,
associated lemmas, syllabation, grammatical category, gender and number,
frequencies in a corpus of books and in a body of film subtitles, etc...

|

Lexique 3.83 est une base de données lexicales du français qui fournit
pour ~140000 mots du français: les représentations orthographiques et
phonémiques, les lemmes associés, la syllabation, la catégorie
grammaticale, le genre et le nombre, les fréquences dans un corpus de
livres et dans un corpus de sous-titres de films, etc...

Table: `Lexique383.zip`_

Web site: http://www.lexique.org

Online: http://www.lexique.org/shiny/lexique

Publications
------------

-  New, Boris, Christophe Pallier, Marc Brysbaert, and Ludovic Ferrand.
   2004. "Lexique 2: A New French Lexical Database." *Behavior Research
   Methods, Instruments, & Computers* 36 (3): 516--524.
   `DOI <https://doi.org/10.3758/bf03195598>`__.
   `pdf`_

-  New, Boris, Christophe Pallier, Ludovic Ferrand, and Rafael Matos.
   2001. "Une Base de Données Lexicales Du Français Contemporain Sur
   Internet: LEXIQUE" *L'Année Psychologique* 101 (3): 447--462.
   `DOI <https://doi.org/10.1017/S014271640707035X>`__.
   `pdf <https://docs.google.com/viewer?url=http://www.lexique.org/outils/Lexique_Annee.pdf>`__

-  Boris New, Marc Brysbaert, Jean Veronis, and Christophe Pallier.
   2007. "The Use of Film Subtitles to Estimate Word Frequencies."
   Applied Psycholinguistics 28 (4): 661--77.
   `DOI <https://doi.org/10.1017/S014271640707035X>`__.
   (`pdf <https://drive.google.com/file/d/1uvKrxGqETXkFeRH4PcYaql8ES9FjEdbV/view?usp=sharing>`__)

Contributors
------------

-  Boris New & Christophe Pallier
-  Ronald Peereman
-  Sophie Dufour
-  Christian Lachaud
-  and many others... (contact us to be listed)

License
-------

`CC BY SA40.0`_

.. _Lexique383.zip: http://www.lexique.org/databases/Lexique383/Lexique383.zip
.. _pdf: https://docs.google.com/viewer?url=http://sites.google.com/site/borisnew/pub/New-et-al2004-BRMIC.pdf?attredirects=0
.. _CC BY SA40.0: LICENSE-CC-BY-SA4.0.txt


BibTex Entry to cite publications about Lexique383:


.. code:: bibtex

    @article{npbf04,
    author = {New, B. and Pallier, C. and Brysbaert, M. and Ferrand, L.},
    journal = {ehavior Research Methods, Instruments, & Computers},
    number = {3},
    pages = {516-524},
    title = {Lexique 2 : A New French Lexical Database},
    volume = {36},
    year = {2004},
    eprint = {http://www.lexique.org/?page_id=294},
    }

.. code:: bibtex

    @article{npfm01,
    author = {New, B. and Pallier, C. and Ferrand, L. and Matos, R.},
    journal = {L'Ann{\'e}e Pschologique},
    number = {447-462},
    pages = {1396-2},
    title = {Une base de donn{\'e}es lexicales du fran\c{c}ais contemporain sur internet: LEXIQUE},
    volume = {101},
    year = {2001},
    }

.. code:: bibtex

    @article{new_brysbaert_veronis_pallier_2007,
    author={NEW, BORIS and BRYSBAERT, MARC and VERONIS, JEAN and PALLIER, CHRISTOPHE},
    title={The use of film subtitles to estimate word frequencies},
    volume={28}, DOI={10.1017/S014271640707035X},
    number={4}, journal={Applied Psycholinguistics},
    publisher={Cambridge University Press},
    year={2007},
    pages={661–677}}

.. _Lexique383: http://www.lexique.org/
.. _SekouDiaoNlp: https://github.com/SekouDiaoNlp
.. _`official documentation of Lexique383`: http://lexique.org/_documentation/Manuel_Lexique.3.2.pdf
