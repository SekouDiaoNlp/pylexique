=====
Usage
=====

.. NOTE:: The language of the lexical entries is French.
    | The cLexical Corpus is based on `Lexique383`_.
    | Also note that pylexique only works on Python 3.X


To use pylexique from the command line:


.. code-block:: bash

    $ pylexique manger

    $ pylexique boire


To use pylexique  as a library in your own projects:


.. code-block:: python

        from pylexique import Lexique383, vdir
        from pprint import pprint
        import pkg_resources

        # Assigns resource paths
        _RESOURCE_PACKAGE = 'pylexique'
        _RESOURCE_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'Lexique383/Lexique383.txt')
        _RESOURCE_PICKLE_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'Lexique383/Lexique383.pkl')

        #  Create new Lexique383 instance with a pre-built Lexique383.
        LEXIQUE = Lexique383()

        # Creates a new Lexique383 instance while supplying your own Lexique38X lexicon. The first time it will it will be
        # slow to parse the file and create a persistent data-store. Next runs should be much faster.
        LEXIQUE2 = Lexique383(_RESOURCE_PATH)


        #  Retrieves the lexical information of 'abaissait' and 'a'.
        var_1 = LEXIQUE.lexique['abaissait']

        # Because in French the world 'a' is very polysemic word, it has several entries in Lexique 383.
        # For this reason the LEXIQUE Dict has the value of the `ortho` property of its LexicalEntry.
        # In th case of 'abaissait' there is only one LexItem corresponding to this dist key.
        #
        # But in the case of 'a' there are several LexItem objects corresponding to this key and then LexItem ojects
        # are stored n a list corresponding to th value of the key.
        var_2 = LEXIQUE.lexique['a']

        pprint(vdir(var_1))
        pprint(vdir(var_2))

        # Get all verbs in the DataSet. Because some words have the same orthography, some keys of the dictionary
        # don't have a unique LexicalItem object as their value, but a list of those.
        verbs = []
        for x in LEXIQUE.values():
            if isinstance(x, list):
                for y in x:
                    if not isinstance(y, list) and y.cgram == 'VER':
                        verbs.append(y)
            elif x.cgram == 'VER':
                verbs.append(x)
            else:
                continue

        print('Groovy!')

Documentation for
_`Lexique383`: http://www.lexique.org
