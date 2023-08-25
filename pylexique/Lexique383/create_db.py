import sqlite3
from pylexique import Lexique383

# Create a SQLite database
db_conn = sqlite3.connect('Lexique383.db')
db_cursor = db_conn.cursor()

# Create tables
db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS lexique (
        ortho TEXT,
        phon TEXT,
        lemme TEXT,
        cgram TEXT,
        genre TEXT,
        nombre TEXT,
        freqlemfilms2 REAL,
        freqlemlivres REAL,
        freqfilms2 REAL,
        freqlivres REAL,
        infover TEXT,
        nbhomogr INTEGER,
        nbhomoph INTEGER,
        islem INTEGER,
        nblettres INTEGER,
        nbphons INTEGER,
        cvcv TEXT,
        p_cvcv TEXT,
        voisorth INTEGER,
        voisphon INTEGER,
        puorth INTEGER,
        puphon INTEGER,
        syll TEXT,
        nbsyll INTEGER,
        cv_cv TEXT,
        orthrenv TEXT,
        phonrenv TEXT,
        orthosyll TEXT,
        cgramortho TEXT,
        deflem REAL,
        defobs INTEGER,
        old20 REAL,
        pld20 REAL,
        morphoder TEXT,
        nbmorph INTEGER,
        sorted_ortho TEXT
    )
''')

# Create indexes
db_cursor.execute('CREATE INDEX IF NOT EXISTS lexique_ortho_idx ON lexique (ortho)')
db_cursor.execute('CREATE INDEX IF NOT EXISTS lexique_lemme_idx ON lexique (lemme)')
db_cursor.execute('CREATE INDEX IF NOT EXISTS lexique_sorted_ortho_idx ON lexique (sorted_ortho)')

# Populate table
lexique = Lexique383()

# Populate lexique table
for ortho, lex_items in lexique.lexique.items():
    sorted_ortho = ''.join(sorted(ortho))
    
    if isinstance(lex_items, list):
        for lex_item in lex_items:
            values = (ortho, lex_item.phon, lex_item.lemme, lex_item.cgram, lex_item.genre,
                      lex_item.nombre, lex_item.freqlemfilms2, lex_item.freqlemlivres,
                      lex_item.freqfilms2, lex_item.freqlivres, lex_item.infover,
                      lex_item.nbhomogr, lex_item.nbhomoph, lex_item.islem,
                      lex_item.nblettres, lex_item.nbphons, lex_item.cvcv,
                      lex_item.p_cvcv, lex_item.voisorth, lex_item.voisphon,
                      lex_item.puorth, lex_item.puphon, lex_item.syll,
                      lex_item.nbsyll, lex_item.cv_cv, lex_item.orthrenv,
                      lex_item.phonrenv, lex_item.orthosyll, lex_item.cgramortho,
                      lex_item.deflem, lex_item.defobs, lex_item.old20,
                      lex_item.pld20, lex_item.morphoder, lex_item.nbmorph, sorted_ortho)
            db_cursor.execute('INSERT INTO lexique VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', values)
    else:
        lex_item = lex_items
        values = (ortho, lex_item.phon, lex_item.lemme, lex_item.cgram, lex_item.genre,
                  lex_item.nombre, lex_item.freqlemfilms2, lex_item.freqlemlivres,
                  lex_item.freqfilms2, lex_item.freqlivres, lex_item.infover,
                  lex_item.nbhomogr, lex_item.nbhomoph, lex_item.islem,
                  lex_item.nblettres, lex_item.nbphons, lex_item.cvcv,
                  lex_item.p_cvcv, lex_item.voisorth, lex_item.voisphon,
                  lex_item.puorth, lex_item.puphon, lex_item.syll,
                  lex_item.nbsyll, lex_item.cv_cv, lex_item.orthrenv,
                  lex_item.phonrenv, lex_item.orthosyll, lex_item.cgramortho,
                  lex_item.deflem, lex_item.defobs, lex_item.old20,
                  lex_item.pld20, lex_item.morphoder, lex_item.nbmorph, sorted_ortho)
        db_cursor.execute('INSERT INTO lexique VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', values)

# Commit changes and close connection
db_conn.commit()
db_conn.close()
