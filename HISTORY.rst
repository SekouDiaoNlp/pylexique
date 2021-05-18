=======
History
=======

1.3.5 (2021-05-18)
------------------

* Uses str.lower() to normalize inputs.
* Updated the Documentation and the docstrings.

1.3.4 (2021-05-16)
------------------

* Fixed bug where Lexique383 was not shipped with the distribution.
* Made csv parsing far faster and more robust.
* Can now use different parsers : 'pandas_csv' is the pandas csv parser, 'std_csv' is the standard library csv parser, 'csv' is a custom csv parser and 'xlsb' is pandas xlsb parser using pyxlsb engine.
* Updated dependencies.

1.3.3 (2021-05-16)
------------------

* Made csv parsing faster and more robust.
* Can now use different parsers : 'pandas_csv' is the pandas csv parser, 'std_csv' is the standard library csv parser, 'csv' is a custom csv parser and 'xlsb' is pandas xlsb parser using pyxlsb engine.
* Updated dependencies.

1.3.2 (2021-05-14)
------------------

* Can now use both 'csv' and 'xlsb' files.
* Uses 'csv' file for storage and faster load times.
* Updated dependencies.

1.3.1 (2021-05-12)
------------------

* Uses pandas for now for faster resource loading.
* Uses xlsb file for storage and faster load times
* Updated dependencies.

1.3.0 (2021-05-11)
------------------

* Uses pandas for now for faster resource loading.
* In the process of integrating `faster-than-csv` when MacOs issues get resolved.
* Refactored and expanded the test suite.
* Updated dependencies.

1.2.7 (2021-05-07)
------------------

* The new method Lexique383.get_all_forms(word) is now accessible through the cli with option '-a' or '--all_forms'.
* This new method returns a list of LexItems having the same root lemma.
* Added sample commands using the new option in the docs.
* Refactored and expanded the test suite.
* Updated dependencies.

1.2.6 (2021-05-06)
------------------

* allows for new style of relative imports.
* Now all the attributes of the LexItem objects are immutable for consistency.
* Added new method Lexique383.get_all_forms(word) to get all the lexical variations of a word.
* This new method returns a list of LexItems having the same root lemma.
* Expanded sample usage of the software in the docs.
* Updated dependencies.

1.2.3 (2021-05-04)
------------------

* Enhanced behaviour of output to stdout to not conflict with the logging strategy of users importing the library in their own projects.
* Expanded sample usage of the software in the docs.
* Updated dependencies.

1.2.2 (2021-05-04)
------------------

* Enhanced Type Hinting for main module.
* Changed the property LexItem.islem to boolean instead of a binary choice 0/1.
* Expanded sample usage of the software in the docs.
* Updated dependencies.

1.2.1 (2021-04-30)
------------------

* Implemented Type Hinting for main module.
* Added a new method to the class Lexique383. The method is Lexique383._save_errors() .
* This new method checks that the value of each field in a LexItem is of the right type. If it finds errors it will record the mismatched value/type and save it in ./erros/errors.json
* Expanded sample usage of the software in the docs.
* Much better documentation including links to Lexique383 pages and manuals.

1.2.0 (2021-04-30)
------------------

* Added a new method to the class Lexique383. The method is Lexique383.get_lex() .
* This new method accepts either a single word as a string or an iterable of strings and will return the asked lexical information.
* Expanded sample usage of the software in the docs.
* Substantial update to the code and docs.
* Removed unneeded dependencies as I reimplement some functionality myself.

1.1.1 (2021-04-28)
------------------

* Added a new method to the class LexItem. The method is LexItem.to_dict() .
* This new method allows the LexItem objects to be converted into dicts with key/value pairs corresponding to the LexItem.
* This method allows easy display or serialization of the LexItem objects.
* Lexical Items having the same orthography are stored in a list at the word's orthography key to the LEXIQUE dict.
* Expanded sample usage of the software in the docs.
* Substantial update to the code and docs.

1.1.0 (2021-04-28)
------------------

* Drastically reduced dependencies by ditching HDF5 and bolcs as the package is now smaller, faster an easier to build.
* Lexical Items having the same orthography are stored in a list at the word's orthography key to the LEXIQUE dict.
* Implemented the "FlyWheel" pattern for light Lexical entries rsiding entirely in memory at run time.
* Added sample usage of the software in the docs.
* General update to the code and docs.

1.0.7 (2021-04-27)
------------------

* First release on PyPI.
