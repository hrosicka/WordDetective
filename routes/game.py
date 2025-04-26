from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
from routes.game_logic import new_game, reveal_random_letter

game_bp = Blueprint('game', __name__)

@game_bp.route("/", methods=["GET", "POST"])
def game():
    if 'secret_word' not in session:
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
        elif len(guess) == len(secret_word) and guess == secret_word:
            session['guessed_letters'] = list(secret_word)
            if not session.get('word_guessed', False):
                # Zde by se volala funkce pro aktualizaci skóre z jiného blueprintu
                # Například: requests.post(url_for('scores.update_score', points=10))
                session['word_guessed'] = True
            session['message'] = f"Congratulations! You guessed the word '{secret_word}'."
        else:
            session['message'] = "Wrong guess. Try again."

        session['attempts_left'] -= 1

        if session['attempts_left'] <= 0 and "_" in guessed_letters:
            session['message'] = f"You lost! The word was '{secret_word}'."
            session['word_guessed'] = False

    return render_template(
        "index.html",
        clues=session['clues'],
        guessed_letters=session['guessed_letters'],
        attempts_left=session['attempts_left'],
        message=session['message']
    )

@game_bp.route("/new_game")
def new():
    new_game(session, current_app.words_with_clues)
    return render_template("index.html",
                           clues=session['clues'],
                           guessed_letters=session['guessed_letters'],
                           attempts_left=session['attempts_left'],
                           message=session['message'])