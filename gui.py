# nanocard_app/gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
from database import create_connection, create_tables, add_deck, add_card, get_decks, get_cards, delete_deck

class NanoCardApp:
    def __init__(self, root):
        self.conn = create_connection('nano_cards.db')
        create_tables(self.conn)

        self.root = root
        self.root.title('NanoCard App')
        self.root.geometry('500x500')

        self.style = Style(theme='litera')
        self.style.configure('TLabel', font=('TkDefaultFont', 18))
        self.style.configure('TButton', font=('TkDefaultFont', 16))

        # We'll use these global variables to look at notecards and browse decks.
        self.deck_name_var = tk.StringVar()
        self.front_var = tk.StringVar()
        self.back_var = tk.StringVar()
        self.existing_deck_var = tk.StringVar()
        self.existing_front_var = tk.StringVar()
        self.existing_back_var = tk.StringVar()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.review_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.review_frame, text='Review')

        self.card_index = 0
        self.current_cards = []

        self.front_label = ttk.Label(self.review_frame, text='', font=('TkDefaultFont', 24))
        self.front_label.pack(padx=5, pady=40)

        self.back_label = ttk.Label(self.review_frame, text='')
        self.back_label.pack(padx=5, pady=5)

        ttk.Button(self.review_frame, text='Flip', command=self.flip_card).pack(side='left', padx=5, pady=5)
        ttk.Button(self.review_frame, text='Next', command=self.next_card).pack(side='right', padx=5, pady=5)
        ttk.Button(self.review_frame, text='Previous', command=self.prev_card).pack(side='right', padx=5, pady=5)

        self.add_card_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_card_frame, text='Add Card to Deck')

        self.existing_decks_combobox = ttk.Combobox(self.add_card_frame, state='readonly', textvariable=self.existing_deck_var)
        self.existing_decks_combobox.pack(padx=5, pady=5)

        ttk.Label(self.add_card_frame, text='Front:').pack(padx=5, pady=5)
        self.existing_front_entry = ttk.Entry(self.add_card_frame, textvariable=self.existing_front_var, width=30)
        self.existing_front_entry.pack(padx=5, pady=5)

        ttk.Label(self.add_card_frame, text='Back:').pack(padx=5, pady=5)
        self.existing_back_entry = ttk.Entry(self.add_card_frame, textvariable=self.existing_back_var, width=30)
        self.existing_back_entry.pack(padx=5, pady=5)

        ttk.Button(self.add_card_frame, text='Add Card', command=self.add_card_to_existing_deck).pack(padx=5, pady=10)

        self.browse_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.browse_frame, text='Browse')

        self.browse_decks_combobox = ttk.Combobox(self.browse_frame, state='readonly')
        self.browse_decks_combobox.pack(padx=5, pady=40)

        ttk.Button(self.browse_frame, text='Select Deck', command=self.select_deck).pack(padx=5, pady=5)
        ttk.Button(self.browse_frame, text='Delete Deck', command=self.delete_selected_deck).pack(padx=5, pady=5)

        self.new_deck_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.new_deck_frame, text='New Deck')

        ttk.Label(self.new_deck_frame, text='Deck Name:').pack(padx=5, pady=5)
        self.deck_name_entry = ttk.Entry(self.new_deck_frame, textvariable=self.deck_name_var, width=30)
        self.deck_name_entry.pack(padx=5, pady=5)

        ttk.Label(self.new_deck_frame, text='Front:').pack(padx=5, pady=5)
        self.front_entry = ttk.Entry(self.new_deck_frame, textvariable=self.front_var, width=30)
        self.front_entry.pack(padx=5, pady=5)

        ttk.Label(self.new_deck_frame, text='Back:').pack(padx=5, pady=5)
        self.back_entry = ttk.Entry(self.new_deck_frame, textvariable=self.back_var, width=30)
        self.back_entry.pack(padx=5, pady=5)

        ttk.Button(self.new_deck_frame, text='Add Card', command=self.add_card_to_deck).pack(padx=5, pady=10)
        ttk.Button(self.new_deck_frame, text='Save Deck', command=self.create_deck).pack(padx=5, pady=10)

        self.populate_decks_combobox()
        self.populate_existing_decks_combobox()
        self.populate_browse_decks_combobox()

    def populate_decks_combobox(self):
        decks = get_decks(self.conn)
        self.browse_decks_combobox['values'] = tuple(decks.keys())
        
    def populate_existing_decks_combobox(self):
        decks = get_decks(self.conn)
        self.existing_decks_combobox['values'] = tuple(decks.keys())

    def populate_browse_decks_combobox(self):
        decks = get_decks(self.conn)
        self.browse_decks_combobox['values'] = tuple(decks.keys())

    def add_card_to_existing_deck(self):
        deck_name = self.existing_deck_var.get()
        front = self.existing_front_var.get()
        back = self.existing_back_var.get()

        if deck_name and front and back:
            decks = get_decks(self.conn)
            deck_id = decks[deck_name]

            add_card(self.conn, deck_id, front, back)

            self.existing_front_var.set('')
            self.existing_back_var.set('')
            messagebox.showinfo('Success', 'Card added to existing deck successfully!')

    def add_card_to_deck(self):
        deck_name = self.deck_name_var.get()
        front = self.front_var.get()
        back = self.back_var.get()

        if deck_name and front and back:
            decks = get_decks(self.conn)
            if deck_name not in decks:
                deck_id = add_deck(self.conn, deck_name)
            else:
                deck_id = decks[deck_name]

            add_card(self.conn, deck_id, front, back)

            self.front_var.set('')
            self.back_var.set('')
            messagebox.showinfo('Success', 'Card added successfully!')

    def create_deck(self):
        self.deck_name_var.set('')
        self.front_var.set('')
        self.back_var.set('')
        self.populate_decks_combobox()
        self.populate_existing_decks_combobox()
        self.populate_browse_decks_combobox()
        messagebox.showinfo('Success', 'Flashcard deck created successfully!')

    def select_deck(self):
        selected_deck_name = self.browse_decks_combobox.get()
        if selected_deck_name:
            decks = get_decks(self.conn)
            deck_id = decks[selected_deck_name]
            self.current_cards = get_cards(self.conn, deck_id)
            self.card_index = 0
            self.display_card()

    def display_card(self):
        if self.current_cards:
            current_card = self.current_cards[self.card_index]
            self.front_label.config(text=current_card[0])
            self.back_label.config(text='')
        else:
            self.front_label.config(text='No cards available')
            self.back_label.config(text='')

    def flip_card(self):
        if self.current_cards:
            current_card = self.current_cards[self.card_index]
            if self.back_label.cget('text'):
                self.back_label.config(text='')
            else:
                self.back_label.config(text=current_card[1])

    def next_card(self):
        if self.current_cards:
            self.card_index = (self.card_index + 1) % len(self.current_cards)
            self.display_card()

    def prev_card(self):
        if self.current_cards:
            self.card_index = (self.card_index - 1) % len(self.current_cards)
            self.display_card()

    def delete_selected_deck(self):
        selected_deck_name = self.browse_decks_combobox.get()
        if selected_deck_name:
            decks = get_decks(self.conn)
            deck_id = decks[selected_deck_name]
            delete_deck(self.conn, deck_id)
            self.populate_decks_combobox()
            self.populate_existing_decks_combobox()
            self.populate_browse_decks_combobox()
            self.current_cards = []
            self.display_card()
            messagebox.showinfo('Success', f'Flashcard deck "{selected_deck_name}" deleted successfully!')
