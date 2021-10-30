from pylexique import Lexique383
from time import time

lexicon = Lexique383()

var_1 = lexicon.lexique['abaissait']
var_1_bis = lexicon.get_lex('abaissait')
var_1_ter = lexicon.get_anagrams('abaisse')
var_1_quart = lexicon.get_anagrams('abaisser')

print('OK')
