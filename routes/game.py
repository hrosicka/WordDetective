from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
from routes.game_logic import new_game, reveal_random_letter
import requests

game_bp = Blueprint('game', __name__)

@game_bp.route("/", methods=["GET", "POST"])
def game():
    """
    Handles the main game page and user interactions.

    GET request: Renders the game interface. Initializes a new game if no 'secret_word' exists in the session.
    POST request: Processes the user's guess, updates the game state in the session, and provides feedback.
    """
    if not current_app.words_with_clues:
        current_app.logger.error('Failed to load words for the game.')
        # If words haven't been loaded successfully, display an error page to the user.
        return render_template('error.html', message='Failed to load words for the game.')

    if 'secret_word' not in session:
        # Initialize a new game if the secret word is not already in the session.
        new_game(session, current_app.words_with_clues)

    if request.method == "POST":
        # Retrieve the user's guess from the form.
        guess = request.form['guess'].lower()
        secret_word = session['secret_word']
        guessed_letters = session['guessed_letters']

        # Handle single letter guesses.
        if len(guess) == 1 and guess in secret_word:
            for i, letter in enumerate(secret_word):
                if letter == guess:
                    guessed_letters[i] = guess
            session['message'] = "Correct letter!"
        # Handle full word guesses.
        elif len(guess) == len(secret_word) and guess == secret_word:
            session['guessed_letters'] = list(secret_word)
            if not session.get('word_guessed', False):
                # Placeholder for calling a function to update the score from another blueprint.
                requests.post(url_for('score.update_score', _external=True), json={'points': 10})
                session['word_guessed'] = True
            session['message'] = f"Congratulations! You guessed the word '{secret_word}'."
            current_app.logger.info(f"User correctly guessed the word: '{secret_word}'")
        # Handle incorrect guesses.
        else:
            session['message'] = "Wrong guess. Try again."
            current_app.logger.info(f"Incorrect guess: '{guess}'")

        # Decrement the number of attempts left.
        session['attempts_left'] -= 1

        # Check if the player has run out of attempts and hasn't guessed the word.
        if session['attempts_left'] <= 0 and "_" in guessed_letters:
            session['message'] = f"You lost! The word was '{secret_word}'."
            session['word_guessed'] = False

    # Render the game page with the current game state.
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
    new_game(session, current_app.words_with_clues)
    return redirect(url_for('game.game')) # Redirect back to the main game page