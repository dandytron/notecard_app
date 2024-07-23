# flashcards_app/database.py
import sqlite3

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS card_decks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deck_id INTEGER NOT NULL,
            front TEXT NOT NULL,
            back TEXT NOT NULL,
            FOREIGN KEY (deck_id) REFERENCES card_decks(id)
        )
    ''')

def add_deck(conn, name):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO card_decks (name)
        VALUES (?)
    ''', (name,))
    deck_id = cursor.lastrowid
    conn.commit()
    return deck_id

def add_card(conn, deck_id, front, back):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO flashcards (deck_id, front, back)
        VALUES (?, ?, ?)
    ''', (deck_id, front, back))
    card_id = cursor.lastrowid
    conn.commit()
    return card_id

def get_decks(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name FROM card_decks
    ''')
    rows = cursor.fetchall()
    decks = {row[1]: row[0] for row in rows}
    return decks

def get_cards(conn, deck_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT front, back FROM flashcards
        WHERE deck_id = ?
    ''', (deck_id,))
    rows = cursor.fetchall()
    cards = [(row[0], row[1]) for row in rows]
    return cards

def delete_deck(conn, deck_id):
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM card_decks
        WHERE id = ?
    ''', (deck_id,))
    conn.commit()