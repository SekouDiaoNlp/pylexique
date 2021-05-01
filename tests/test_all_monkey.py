import pytest
from pylexique import Lexique383
from pprint import pprint
import pkg_resources



class TestAll:
    def test_all(self):
        # Assigns resource paths
        _RESOURCE_PACKAGE = 'pylexique'
        _RESOURCE_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'Lexique383/Lexique383.txt')
        _RESOURCE_PICKLE_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'Lexique383/Lexique383.pkl')

        #  Create new Lexique383 instance with a pre-built Lexique383.
        LEXIQUE = Lexique383()

        # Creates a new Lexique383 instance while supplying your own Lexique38X lexicon. The first time it will it will be
        # slow to parse the file and create a persistent data-store. Next runs should be much faster.
        # LEXIQUE2 = Lexique383(_RESOURCE_PATH)

        # There are 2 ways to access the lexical information of a word:
        # Either use the utility method Lexique383.get_lex(item)
        # Or you an directly access the lexicon directory through LEXIQUE.lexique[item] .

        # Notice that item can be either a string or a sequence of strings when using Lexique383.get_lex(item) .


        #  Retrieves the lexical information of 'abaissait' and 'a'.
        var_1 = LEXIQUE.lexique['abaissait']
        var_1_bis = LEXIQUE.get_lex('abaissait')

        # Check both objects are the same
        var_1_equality = var_1 == var_1_bis['abaissait']
        print(var_1_equality)

        # Because in French the world 'a' is very polysemic word, it has several entries in Lexique 383.
        # For this reason the LEXIQUE Dict has the value of the `ortho` property of its LexicalEntry.
        # In th case of 'abaissait' there is only one LexicalItem corresponding to this dist key.
        # But in the case of 'a' there are several LexItem objects corresponding to this key and then the LexItem objects
        # are stored in a list corresponding to th value of the key.
        var_2 = LEXIQUE.lexique['a']
        var_2_bis = LEXIQUE.get_lex('a')

        # Check both objects are the same
        var_2_equality = var_2 == var_2_bis['a']
        print(var_2_equality)

        # Retrieving the lexical information of several words by passing a Sequence of strings

        var_multiple = LEXIQUE.get_lex(('il', 'mange', 'une', 'baguette'))
        pprint(var_multiple)

        # You can use the method LexItem.to_dict() to produce a dictionary with key/value pairs corresponding to the LexItem

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
        pass
