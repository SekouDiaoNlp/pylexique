=====
Usage
=====

.. NOTE:: The language of the lexical entries is French.
    The Lexical Corpus is based on `Lexique383`_.
    Also note that pylexique only works on Python 3.X.


To use pylexique from the command line:
---------------------------------------


.. code-block:: bash

    $ pylexique manger

The output will be a json representation of the LexItem objects:

.. code-block:: json

    {
        "manger": [
            [
                {
                    "ortho": "manger",
                    "phon": "m@Ze",
                    "lemme": "manger",
                    "cgram": "NOM",
                    "genre": "m",
                    "nombre": "s",
                    "freqlemfilms2": 5.62,
                    "freqlemlivres": 4.05,
                    "freqfilms2": 5.62,
                    "freqlivres": 4.05,
                    "infover": "",
                    "nbhomogr": 2,
                    "nbhomoph": 7,
                    "islem": True,
                    "nblettres": 6,
                    "nbphons": 4,
                    "cvcv": "CVCCVC",
                    "p_cvcv": "CVCV",
                    "voisorth": 9,
                    "voisphon": 12,
                    "puorth": 6,
                    "puphon": 4,
                    "syll": "m@-Ze",
                    "nbsyll": 2,
                    "cv_cv": "CV-CV",
                    "orthrenv": "regnam",
                    "phonrenv": "eZ@m",
                    "orthosyll": "man-ger",
                    "cgramortho": "NOM,VER",
                    "deflem": "100",
                    "defobs": "33",
                    "old20": 1.35,
                    "pld20": 1.25,
                    "morphoder": "manger",
                    "nbmorph": "1"
                },
                {
                    "ortho": "manger",
                    "phon": "m@Ze",
                    "lemme": "manger",
                    "cgram": "VER",
                    "genre": "",
                    "nombre": "",
                    "freqlemfilms2": 467.82,
                    "freqlemlivres": 280.61,
                    "freqfilms2": 207.63,
                    "freqlivres": 134.26,
                    "infover": "\"inf;;\"",
                    "nbhomogr": 2,
                    "nbhomoph": 7,
                    "islem": True,
                    "nblettres": 6,
                    "nbphons": 4,
                    "cvcv": "CVCCVC",
                    "p_cvcv": "CVCV",
                    "voisorth": 9,
                    "voisphon": 12,
                    "puorth": 6,
                    "puphon": 4,
                    "syll": "m@-Ze",
                    "nbsyll": 2,
                    "cv_cv": "CV-CV",
                    "orthrenv": "regnam",
                    "phonrenv": "eZ@m",
                    "orthosyll": "man-ger",
                    "cgramortho": "NOM,VER",
                    "deflem": "100",
                    "defobs": "20",
                    "old20": 1.35,
                    "pld20": 1.25,
                    "morphoder": "manger",
                    "nbmorph": "1"
                }
            ]
        ]
    }


.. code-block:: bash

    $ pylexique boire


.. code-block:: json

    {
        "boire": [
            [
                {
                    "ortho": "boire",
                    "phon": "bwaR",
                    "lemme": "boire",
                    "cgram": "NOM",
                    "genre": "m",
                    "nombre": "s",
                    "freqlemfilms2": 2.67,
                    "freqlemlivres": 2.03,
                    "freqfilms2": 2.67,
                    "freqlivres": 2.03,
                    "infover": "",
                    "nbhomogr": 2,
                    "nbhomoph": 2,
                    "islem": True,
                    "nblettres": 5,
                    "nbphons": 4,
                    "cvcv": "CVVCV",
                    "p_cvcv": "CYVC",
                    "voisorth": 9,
                    "voisphon": 14,
                    "puorth": 4,
                    "puphon": 4,
                    "syll": "bwaR",
                    "nbsyll": 1,
                    "cv_cv": "CYVC",
                    "orthrenv": "eriob",
                    "phonrenv": "Rawb",
                    "orthosyll": "boi-re",
                    "cgramortho": "NOM,VER",
                    "deflem": "96",
                    "defobs": "30",
                    "old20": 1.4,
                    "pld20": "1",
                    "morphoder": "boire",
                    "nbmorph": "1"
                },
                {
                    "ortho": "boire",
                    "phon": "bwaR",
                    "lemme": "boire",
                    "cgram": "VER",
                    "genre": "",
                    "nombre": "",
                    "freqlemfilms2": 339.05,
                    "freqlemlivres": 274.32,
                    "freqfilms2": 142.15,
                    "freqlivres": 100.27,
                    "infover": "\"inf;;\"",
                    "nbhomogr": 2,
                    "nbhomoph": 2,
                    "islem": True,
                    "nblettres": 5,
                    "nbphons": 4,
                    "cvcv": "CVVCV",
                    "p_cvcv": "CYVC",
                    "voisorth": 9,
                    "voisphon": 14,
                    "puorth": 4,
                    "puphon": 4,
                    "syll": "bwaR",
                    "nbsyll": 1,
                    "cv_cv": "CYVC",
                    "orthrenv": "eriob",
                    "phonrenv": "Rawb",
                    "orthosyll": "boi-re",
                    "cgramortho": "NOM,VER",
                    "deflem": "100",
                    "defobs": "30",
                    "old20": 1.4,
                    "pld20": "1",
                    "morphoder": "boire",
                    "nbmorph": "1"
                }
            ]
        ]
    }

You can also provide multiple words and/or specify an output file to save the lexical information in a json file.

.. code-block:: bash

    $ pylexique il mange une baguette

    $ pylexique il boit du vin rouge -o path/to/the/output/json/file.json

The output will be similar as previously, with a json entry for each word in the sequence.

|

You can also retrieve all the lexical forms of the provided word/words by using the option '-a' or '--all_forms'

.. code-block:: bash

    $ pylexique il mange une baguette -a

    $ pylexique il boit du vin rouge -o path/to/the/output/json/file.json --all_forms

|

To use pylexique  as a library in your own projects:
----------------------------------------------------


.. code-block:: python

        from pylexique import Lexique383
        from pprint import pprint

        #  Create new Lexique383 instance with a pre-built Lexique383.
        LEXIQUE = Lexique383()

        # Creates a new Lexique383 instance while supplying your own Lexique38X lexicon. The first time it will it will be
        # slow to parse the file and create a persistent data-store. Next runs should be much faster.
        RESOURCE_PATH = 'path/to/Lexique38x'
        # parser_type must be either omitted if RESOURCE_PATH is a csv file and you want to use the default csv parser.
        # if parser_type is provided it should be either 'xlsb', 'pandas_csv', 'csv', 'std_csv'. 'std_csv' is used by default.
        LEXIQUE2 = Lexique383(RESOURCE_PATH, parser_type='std_csv')


There are 2 ways to access the lexical information of a word:
Either use the utility method Lexique383.get_lex(item)
Or you can directly access the lexicon directory through LEXIQUE.lexique[item] .

Notice that item can be either a string or a sequence of strings when using Lexique383.get_lex(item) .


 .. code-block:: python

        #  Retrieves the lexical information of 'abaissait' and 'a'.
        var_1 = LEXIQUE.lexique['abaissait']
        var_1_bis = LEXIQUE.get_lex('abaissait')

        # Check both objects are the same
        var_1_equality = var_1 == var_1_bis['abaissait']
        print(var_1_equality)



Because in French the world 'a' is a very polysemic word, it has several entries in Lexique 383.
For this reason the LEXIQUE Dict has the value of the `ortho` property of its LexicalEntry.
In th case of 'abaissait' there is only one LexicalItem corresponding to this dict key.
But in the case of 'a' there are several LexItem objects corresponding to this key and then the LexItem objects
are stored in a list corresponding to th value of the key.

 .. code-block:: python

        var_2 = LEXIQUE.lexique['a']
        var_2_bis = LEXIQUE.get_lex('a')

        # Check both objects are the same
        var_2_equality = var_2 == var_2_bis['a']
        print(var_2_equality)

        # Retrieving the lexical information of several words by passing a Sequence of strings

        var_multiple = LEXIQUE.get_lex(('il', 'mange', 'une', 'baguette'))
        pprint(var_multiple)

You can get all the forms of a given word by calling the method Lexique383.get_all_forms(word):

 .. code-block:: python

        all_avoir_forms = LEXIQUE.get_all_forms('avez')
        print(len(all_avoir_forms))

        print('\n')

        all_vouloir_forms = LEXIQUE.get_all_forms('voulu')
        print(len(all_vouloir_forms))


You can use the method LexItem.to_dict() to produce a dictionary with key/value pairs corresponding to the LexItem


 .. code-block:: python

        print('\n\n')
        if isinstance(var_1, list):
            for elmt in var_1:
                pprint(elmt.to_dict())
                print('\n\n')
        else:
            pprint(var_1.to_dict())
            print('\n\n')

        print('\n\n')
        if isinstance(var_2, list):
            for elmt in var_2:
                pprint(elmt.to_dict())
                print('\n\n')
        else:
            pprint(var_2.to_dict())
            print('\n\n')

        # Get all verbs in the DataSet. Because some words have the same orthography, some keys of the dictionary
        # don't have a unique LexItem object as their value, but a list of those.
        verbs = []
        for x in LEXIQUE.lexique.values():
            if isinstance(x, list):
                for y in x:
                    if not isinstance(y, list) and y.cgram == 'VER':
                        verbs.append(y)
            elif x.cgram == 'VER':
                verbs.append(x)
            else:
                continue

        print('Printing the first 5 verbs found in the preceding search:')
        pprint(verbs[0:5])

        # Print the first 5 verbs with full lexical information.
        for verb in verbs[0:5]:
            pprint(verb.to_dict())


Documentation for
_`Lexique383`: http://www.lexique.org
