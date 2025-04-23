from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import random
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # A secret key is needed to work with sessions

SCORE_FILE = 'scores.json'

with open('data.json', 'r', encoding='utf-8') as f:
    words_with_clues = json.load(f)

def new_game():
    """Initializes a new game."""
    secret_word = random.choice(list(words_with_clues.keys()))
    clues = words_with_clues[secret_word]
    attempts_left = 7
    guessed_letters = ["_" for _ in secret_word]
    session['secret_word'] = secret_word
    session['clues'] = clues
    session['attempts_left'] = attempts_left
    session['guessed_letters'] = guessed_letters
    session['message'] = ""

def reveal_random_letter():
    """Reveals a random hidden letter in the secret word."""
    hidden_indices = [i for i, letter in enumerate(session['guessed_letters']) if letter == "_"]
    if hidden_indices:
        random_index = random.choice(hidden_indices)
        secret_word = session['secret_word']
        session['guessed_letters'][random_index] = secret_word[random_index]

# Funkce pro načtení skóre
def load_scores():
    try:
        with open(SCORE_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"player_scores": {}}

# Funkce pro uložení skóre
def save_scores(data):
    with open(SCORE_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@app.route("/", methods=["GET", "POST"])
def game():
    if 'secret_word' not in session:
        new_game()

    if request.method == "POST":
        guess = request.form['guess'].lower()
        secret_word = session['secret_word']
        attempts_left = session['attempts_left']
        guessed_letters = session['guessed_letters']

        if len(guess) == 1:
            if guess in secret_word:
                for i, letter in enumerate(secret_word):
                    if letter == guess:
                        guessed_letters[i] = guess
                session['message'] = "Correct letter!"
            else:
                attempts_left -= 1
                reveal_random_letter()
                session['message'] = f"Wrong letter. You have {attempts_left} attempts left."
        elif len(guess) == len(secret_word):
            if guess == secret_word:
                session['message'] = f"Congratulations! You guessed the word '{secret_word}'."
                guessed_letters = secret_word
                session['attempts_left'] = 0  # End the game
            else:
                attempts_left -= 1
                session['message'] = f"Wrong word guess. You have {attempts_left} attempts left."
        else:
            session['message'] = "Please enter a single letter or the whole word."

        session['attempts_left'] = attempts_left
        session['guessed_letters'] = guessed_letters

        if attempts_left <= 0 and "".join(session['guessed_letters']) != secret_word:
            session['message'] = f"You lost. The secret word was '{secret_word}'."

    return render_template("index.html",
                           clues=session['clues'],
                           guessed_letters=session['guessed_letters'],
                           attempts_left=session['attempts_left'],
                           message=session['message'])

@app.route("/new_game")
def new():
    new_game()
    return render_template("index.html",
                           clues=session['clues'],
                           guessed_letters=session['guessed_letters'],
                           attempts_left=session['attempts_left'],
                           message=session['message'])

@app.route('/add_word', methods=['GET', 'POST'])
def add_word():
    message = None
    if request.method == 'POST':
        word = request.form['word']
        description = request.form['description']

        try:
            with open('data.json', 'r+', encoding='utf-8') as file:
                # Load the content of the file
                try:
                    data = json.load(file)
                    if not isinstance(data, dict):
                        raise ValueError("The content of data.json is not a dictionary!")
                except json.JSONDecodeError:
                    # If the file is empty, initialize as an empty dictionary
                    data = {}

                # Add the new word to the dictionary
                if word in data:
                    message = f"The word '{word}' already exists!"
                
                else:
                    data[word] = description
                    # Write back to the file
                    file.seek(0)
                    json.dump(data, file, ensure_ascii=False, indent=4)
                    file.truncate()  # Remove any remaining content
                    return redirect(url_for('index'))  # Redirect to the main page
        except Exception as e:
            message = f"Error during saving: {str(e)}"

    return render_template('add_word.html', message=message)  # Display the form

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview', methods=['GET'])
def preview():
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return render_template('preview.html', data=data)

@app.route('/update_score', methods=['POST'])
def update_score():
    # Načtení dat ze skóre
    data = load_scores()
    scores = data["player_scores"]

    # Získání jména hráče a bodů z požadavku
    player = request.json.get('player', 'Guest')  # Výchozí hráč je "Guest"
    points = request.json.get('points', 0)

    # Aktualizace skóre hráče
    if player in scores:
        scores[player] += points
    else:
        scores[player] = points

    # Uložení aktualizovaného skóre
    save_scores(data)

    return jsonify({"message": f"Updated score for {player}", "scores": scores})

@app.route('/scores', methods=['GET'])
def get_scores():
    # Vrácení aktuálního skóre
    data = load_scores()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)