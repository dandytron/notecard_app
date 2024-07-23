# NanoCard v. 0.8

## Description
NanoCard is a basic notecard review app that lets you:

- Create a deck of flashcards with anything on their front and back, card-by-card
- Review those cards
- Add new ones to the deck
- Browse your decks

NanoCard uses Python's built-in sqlite3 to store and retrieve the card decks. 
In its current build its best used for small, light material to review as its ability to let you edit your decks is relatively basic.

## Future features

If I revisit this project, there are a few tweaks I'd like to make:

- Make better use of tkinter's grid features for a more dynamic interface
- Deeper functions to edit and amend decks and cards
- A spaced reptetition feature for better review of material

## Requirements
- Python 3.12+
- ttkboostrap 1.10.1

## Installation

### Clone the Repository

To clone the repository to your local machine, open your terminal and run:

```
sh
git clone https://github.com/yourusername/my-linux-project.git
cd nanocard_app
```

#### SETUP VIRTUAL ENVIRONMENT (OPTIONAL BUT RECOMMENDED)

It's a good practice to create a virtual environment for your project to manage dependencies. Here's how to set one up using venv:

```
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

#### INSTALL DEPENDENCIES

Once your virtual environment is activated (if you created one), install the required dependencies using pip:

```
pip install -r requirements.txt
```

#### RUNNING THE APPLICATION

To start the application, run the following command in your project directory:

```
python main.py
```


MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
