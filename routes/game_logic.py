import random
import json

def load_words(file_path):
    """Načte slova a nápovědy ze souboru JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def new_game(session, words_with_clues):
    """Inicializuje novou hru."""
    secret_word = random.choice(list(words_with_clues.keys()))
    session['secret_word'] = secret_word
    session['clues'] = words_with_clues[secret_word]
    session['attempts_left'] = 7
    session['guessed_letters'] = ["_" for _ in secret_word]
    session['message'] = ""
    session['word_guessed'] = False

def reveal_random_letter(session):
    """Odhalí náhodné skryté písmeno v tajném slově."""
    hidden_indices = [i for i, letter in enumerate(session['guessed_letters']) if letter == "_"]
    if hidden_indices:
        random_index = random.choice(hidden_indices)
        secret_word = session['secret_word']
        session['guessed_letters'][random_index] = secret_word[random_index]