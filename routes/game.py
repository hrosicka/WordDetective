from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
from routes.game_logic import new_game, reveal_random_letter
import requests
import logging

logger = logging.getLogger('app')

game_bp = Blueprint('game', __name__)

@game_bp.route("/", methods=["GET", "POST"])
def game():
    """
    Handles the main game page and user interactions.

    GET request: Renders the game interface. Initializes a new game if 'secret_word'
                 is not present in the session.
    POST request: Processes the user's guess, updates the game state in the session,
                  and provides feedback to the user.
    """
    if not current_app.words_with_clues:
        logger.error('Failed to load words for the game.')
        return render_template('error.html', message='Failed to load words for the game.')

    if 'secret_word' not in session:
        logger.info('Initializing a new game.')
        new_game(session, current_app.words_with_clues)

    if request.method == "POST":
        guess = request.form['guess'].lower()
        secret_word = session['secret_word']
        guessed_letters = session['guessed_letters']

        if len(guess) == 1 and guess in secret_word:
            for i, letter in enumerate(secret_word):
                if letter == guess:
                    guessed_letters[i] = guess
            session['message'] = "Correct letter!"
            logger.info(f"Correctly guessed letter: '{guess}'.")
        elif len(guess) == len(secret_word) and guess == secret_word:
            session['guessed_letters'] = list(secret_word)
            if not session.get('word_guessed', False):
                try:
                    response = requests.post(url_for('score.update_score', _external=True), json={'points': 10})
                    response.raise_for_status() # Raise an exception for HTTP errors
                    logger.info(f"Score updated successfully. Response status: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    logger.error(f"Error updating score: {e}")
                session['word_guessed'] = True
            session['message'] = f"Congratulations! You guessed the word '{secret_word}'."
            logger.info(f"User correctly guessed the word: '{secret_word}'.")
        else:
            session['message'] = "Wrong guess. Try again."
            logger.info(f"Incorrect guess: '{guess}'.")

        session['attempts_left'] -= 1
        logger.info(f"Attempt made. Attempts left: {session['attempts_left']}.")

        if session['attempts_left'] <= 0 and "_" in guessed_letters:
            session['message'] = f"You lost! The word was '{secret_word}'."
            session['word_guessed'] = False
            logger.info(f"Game over. The secret word was '{secret_word}'.")

    return render_template(
        "index.html",
        clues=session['clues'],
        guessed_letters=session['guessed_letters'],
        attempts_left=session['attempts_left'],
        message=session['message']
    )

@game_bp.route("/new_game")
def new():
    """
    Initializes a new game and redirects the user to the main game page.
    """
    logger.info("Starting a new game via /new_game endpoint.")
    new_game(session, current_app.words_with_clues)
    return redirect(url_for('game.game'))