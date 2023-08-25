import sqlite3

# Connect to the SQLite database
db_conn = sqlite3.connect('lexique_database.db')
db_cursor = db_conn.cursor()

def get_rows_matching_ortho(ortho):
    query = "SELECT * FROM lexique WHERE ortho = ?"
    db_cursor.execute(query, (ortho,))
    return db_cursor.fetchall()

def get_rows_matching_lemmes(ortho):
    query = "SELECT lemme FROM lexique WHERE ortho = ?"
    db_cursor.execute(query, (ortho,))
    lemmes = db_cursor.fetchall()
    
    if not lemmes:
        return []
    
    query = "SELECT * FROM lexique WHERE lemme IN ({})".format(', '.join('?' for _ in lemmes))
    db_cursor.execute(query, lemmes)
    return db_cursor.fetchall()

def get_anagrams(ortho):
    query = "SELECT * FROM lexique WHERE sorted_ortho = ?"
    db_cursor.execute(query, (''.join(sorted(ortho)),))
    return db_cursor.fetchall()

# Example usage
ortho = "example"
matching_rows = get_rows_matching_ortho(ortho)
print("Matching rows for {}: {}".format(ortho, matching_rows))

lemme_rows = get_rows_matching_lemmes(ortho)
print("Lemme rows for {}: {}".format(ortho, lemme_rows))

anagrams = get_anagrams(ortho)
print("Anagrams of {}: {}".format(ortho, anagrams))

# Close the connection
db_conn.close()
