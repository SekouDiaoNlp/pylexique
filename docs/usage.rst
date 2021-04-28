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

    from pylexique import LEXIQUE

    LEXIQUE['abaissait']


    LEXIQUE['a']

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


Documentation for
_`Lexique383`: http://www.lexique.or
