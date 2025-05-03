import random
import json
import logging

logger = logging.getLogger('app')

def load_words(file_path):
    """Loads words and their clues from a JSON file."""
    logger.info(f"Loading words from: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            words_data = json.load(f)
            logger.info(f"Successfully loaded {len(words_data)} words.")
            return words_data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON format in: {file_path}")
        return {}

def new_game(session, words_with_clues):
    """Initializes a new game."""
    if not words_with_clues:
        logger.warning("No words available to start a new game.")
        session['message'] = "No words available. Cannot start a new game."
        return

    secret_word = random.choice(list(words_with_clues.keys()))
    session['secret_word'] = secret_word
    session['clues'] = words_with_clues[secret_word]
    session['attempts_left'] = 7
    session['guessed_letters'] = ["_" for _ in secret_word]
    session['message'] = "New game started. Good luck!"
    session['word_guessed'] = False
    logger.info(f"New game started. Secret word: '{secret_word}', clues: {session['clues']}")

def reveal_random_letter(session):
    """Reveals a random hidden letter in the secret word."""
    hidden_indices = [i for i, letter in enumerate(session['guessed_letters']) if letter == "_"]
    if hidden_indices:
        random_index = random.choice(hidden_indices)
        secret_word = session['secret_word']
        session['guessed_letters'][random_index] = secret_word[random_index]
        logger.info(f"Revealed letter '{secret_word[random_index]}' at index {random_index}.")
    else:
        logger.info("No hidden letters left to reveal.")