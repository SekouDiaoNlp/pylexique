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

        from pylexique import Lexique383
        from pprint import pprint
        import pkg_resources

        # Assigns resource paths
        _RESOURCE_PACKAGE = 'pylexique'
        _RESOURCE_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'Lexique383/Lexique383.txt')

        #  Create new Lexique383 instance with a pre-built and compressed Lexique383. It is blazingly fat.
        # LEXIQUE = Lexique383()

        # Creates a new Lexique383 instance while supplying your own Lexique38X lexicon. The first time it will it will be
        # slow to parse the file and create a persistent data-store. Next runs should be much faster.
        LEXIQUE = Lexique383(_RESOURCE_PATH).lexique

        #  Retrieves the lexical information of 'abaissait' and 'a'.
        var_1 = LEXIQUE['abaissait']

        # Because in French the world 'a' is very polysemic word, it has several entries in Lexique 383.
        # For this reason the LEXIQUE Dict has the value of the `ortho` property of its LexicalEntry.
        # In th case of 'abaissait' there is only one LexicalItem corresponding to this dist key.
        # But in the case of 'a' there are several LexixalEntry objects corresonding to this key and then LexicalEnty onjects
        # are stored n a list corresponding to th value of the key.
        var_2 = LEXIQUE['a']

        pprint(var_1)
        pprint(var_2)

        #  Get all verbs in the DataSet. Because some words have the same orthography, some keys of the dictionary
        #  don't have a unique LexicalItem object as their value, but a list of those.
        verbs = []
        for x in LEXIQUE.values():
            if isinstance(x, list):
                for y in x:
                    if not isinstance(y, list) and y.cgram == 'VER':
                        verbs.append(y)
                        if isinstance(y, list):
                            for z in y:
                                if not isinstance(z, list) and y.cgram == 'VER':
                                    try:
                                        verbs.append(z)
                                    except AttributeError:
                                        print("Yo Dawg, I heard you like verbs, so I put verbs inside verbs!")
                                        continue
            elif x.cgram == 'VER':
                verbs.append(x)
            else:
                continue
        print(verbs)
        pass

Documentation for
_`Lexique383`: http://www.lexique.org
