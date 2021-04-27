=====
Usage
=====

.. NOTE:: The language of the lexical entries is French.
    The cLexical Corpus is based on `Lexique383`_.


To use pylexique from the command line:


.. code-block:: bash

    $ pylexique manger

    $ pylexique boire


To use pylexique  as a library in your own projects:


.. code-block:: python

    from pylexique import LEXIQUE

    for x in LEXIQUE .values():
        if x.cgram == 'VER':
            assert x.cgram == 'VER'
        else:
            others.append(x)

Documentation for
_`Lexique383`: http://www.lexique.or
