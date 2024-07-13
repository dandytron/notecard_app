from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
import sqlite3

# Connect to the SQL database and create tables
 

class Window:
    # constructor should take a width and height in pixels
    def __init__(self, width=400, height=450):

        # Connect to the SQLite database, create tables
        conn = sqlite3.connect('nanocards.db')
        create_tables(conn)

        self.__width = width
        self.__height = height

        # creates a new root widget using ThemedTk() save as private data member
        # Using ThemedTk instead of Tk() lets us pass in the theme we want from ttkthemes
        self.__root = ThemedTk(theme='plastik')

        # set the title property of the root widget
        self.__root.title('NanoCard')

        # sets the width and height of the window
        self.__root.geometry(f'{self.__width}x{self.__height}')

        # sets minimum size for the window
        self.__root.minsize(self.__width, self.__height)


        # Variables for user input
        deck_name_var = StringVar
        front_var = StringVar
        back_var = StringVar

        # A Notebook tkinter widget will be our navigation bar
        notebook = ttk.Notebook(self.__root)
        notebook.pack(fill='both', expand=True)

        # Create the "Review" tab
        review_frame = ttk.Frame(notebook)
        notebook.add(review_frame, text="Review")

        # Create the "Add Card" tab
        add_frame = ttk.Frame(notebook)
        notebook.add(add_frame, text="Add")

        # Create the "Decks" tab
        decks_frame = ttk.Frame(notebook)
        notebook.add(decks_frame, text="Browse")

        # Create the "New" tab
        new_frame = ttk.Frame(notebook)
        notebook.add(new_frame, text="New Deck")


        ### REVIEW TAB (review_frame)
        # Keeping track of where you are in a deck
        card_index = 0
        current_tabs = []

        # Display content on flashcards
        front_label = ttk.Label(review_frame, text='', font=('TkDefaultFont', 24))
        front_label.pack(padx=5, pady=40)
        
        back_label = ttk.Label(review_frame, text='', font=('TkDefaultFont', 24))
        back_label.pack(padx=5, pady=40)


        # Navigation buttons - *****create a new frame for this!
        # (command=last_card)
        ttk.Button(review_frame, text='Last').pack(side='left', padx=5, pady=5)
        # (command=next_card)
        ttk.Button(review_frame, text='Next').pack(side='left', padx=5, pady=5)
        # (command=flip_card)
        ttk.Button(review_frame, text='Flip').pack(side='right', padx=5, pady=5)


        ## ADD TAB (add_frame)
        ttk.Label(add_frame, text='Front:').pack(padx=5,pady=5)
        ttk.Entry(add_frame, textvariable=front_var, width=30).pack(padx=5,pady=5)

        ttk.Label(add_frame, text='Back:').pack(padx=5,pady=5)
        ttk.Entry(add_frame, textvariable=back_var, width=30).pack(padx=5,pady=5)

        ttk.Button(add_frame, text="Add Card").pack(padx=5,pady=10)


        ### DECKS TAB (decks_frame)
        # Combobox widget for selecting an already-made deck
        decks_combobox = ttk.Combobox(decks_frame, state='readonly')
        decks_combobox.pack(padx=5,pady=40)

        # Button for selecting an already-made deck
        ttk.Button(decks_frame, text='Select Deck').pack(padx=5, pady=5)

        # Button to delete a deck
        ttk.Button(decks_frame, text="Delete Deck").pack(padx=5, pady=5)


        ### NEW TAB (new_frame)
        # Label and Entry widgets for 'New' tab:
        # names, words, and definitions
        ttk.Label(new_frame, text='Deck Name:').pack(padx=5,pady=5)
        ttk.Entry(new_frame, textvariable=deck_name_var, width=30).pack(padx=5,pady=5)


        ttk.Label(new_frame, text='Front:').pack(padx=5,pady=5)
        ttk.Entry(new_frame, textvariable=front_var, width=30).pack(padx=5,pady=5)

        ttk.Label(new_frame, text='Back:').pack(padx=5,pady=5)
        ttk.Entry(new_frame, textvariable=back_var, width=30).pack(padx=5,pady=5)

        ttk.Button(new_frame, text="Add Card").pack(padx=5,pady=10)

        ttk.Button(new_frame, text="Save Set").pack(padx=5,pady=10)


    def mainloop(self):
        self.__root.mainloop()


# Use sqlite to create deck and card tables
def create_tables(conn):
    cursor = conn.cursor()

    # Create nanocards_decks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS card_decks (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL
        )  
    ''')

    # Create cards table with foreign_key
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   deck_id INTEGER NOT NULL,
                   front TEXT NOT NULL,
                   back TEXT NOT NULL,
                   FOREIGN KEY (deck_id) REFERENCES card_decks(id)             
        )
    ''')

# logic for how to create a new deck

def add_deck(conn, name):
    cursor = conn.cursor()

    # Insert the name of the deck into the database
    cursor.execute('''
        INSERT INTO card_decks (name)
        VALUES (?)
                   ''', (name,))
    
    deck_id = cursor.lastrowid
    conn.commit()

    return deck_id