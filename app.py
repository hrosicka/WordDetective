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
    session['secret_word'] = secret_word
    session['clues'] = words_with_clues[secret_word]
    session['attempts_left'] = 7
    session['guessed_letters'] = ["_" for _ in secret_word]
    session['message'] = ""
    session['word_guessed'] = False  # Reset příznaku

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
        guessed_letters = session['guessed_letters']

        if len(guess) == 1 and guess in secret_word:
            # Zkontrolujte, zda je písmeno ve slově
            for i, letter in enumerate(secret_word):
                if letter == guess:
                    guessed_letters[i] = guess
            session['message'] = "Correct letter!"
        elif len(guess) == len(secret_word) and guess == secret_word:
            # Pokud uživatel uhodne celé slovo
            session['guessed_letters'] = list(secret_word)
            if not session.get('word_guessed', False):  # Body se přičtou pouze jednou
                update_score(10)  # Aktualizujte skóre
                session['word_guessed'] = True  # Nastavte příznak, že slovo bylo uhádnuto
            session['message'] = f"Congratulations! You guessed the word '{secret_word}'."
        else:
            session['message'] = "Wrong guess. Try again."

        session['attempts_left'] -= 1

        if session['attempts_left'] <= 0 and "_" in guessed_letters:
            session['message'] = f"You lost! The word was '{secret_word}'."
            session['word_guessed'] = False  # Reset příznaku pro nové kolo

    return render_template(
        "index.html",
        clues=session['clues'],
        guessed_letters=session['guessed_letters'],
        attempts_left=session['attempts_left'],
        message=session['message']
    )

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
                    return render_template('add_word.html')
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
def update_score(points):
    # Načtení dat ze skóre
    data = load_scores()
    scores = data["player_scores"]

    # Získání aktuálního hráče ze session
    player = session.get('player_name', 'Guest')

    # Aktualizace skóre pro aktuálního hráče
    if player in scores:
        scores[player] += points
    else:
        scores[player] = points

    # Uložení aktualizovaného skóre
    save_scores(data)

    # Uložení aktualizovaného skóre
    save_scores(data)

    return jsonify({"message": f"Updated score for {player}", "scores": scores})

@app.route('/scores', methods=['GET'])
def get_scores():
    # Načtení dat ze skóre
    data = load_scores()
    player = session.get('player_name', 'Guest')  # Výchozí hráč je "Guest"
    score = data["player_scores"].get(player, 0)
    return jsonify({"player": player, "score": score})

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    data = load_scores()  # Načíst data ze scores.json
    sorted_scores = sorted(data["player_scores"].items(), key=lambda x: x[1], reverse=True)
    return render_template('leaderboard.html', leaderboard=sorted_scores)  # Přesměrování na šablonu

@app.route('/change_name', methods=['GET', 'POST'])
def change_name():
    if request.method == 'POST':
        selected_player = request.form.get('selected_player')
        new_player_name = request.form.get('new_player_name')

        session['player_name'] = new_player_name if new_player_name else selected_player
        session['word_guessed'] = False  # Reset příznaku při změně uživatele
        return redirect(url_for('game'))

    scores = load_scores()
    return render_template('change_name.html', players=scores['player_scores'])


@app.route('/update_name', methods=['POST'])
def update_name():
    new_name = request.form.get('player_name', 'Guest')
    session['player_name'] = new_name  # Uložení jména do session

    # Zde můžete aktualizovat i JSON soubor scores.json, pokud je potřeba
    data = load_scores()
    if 'Guest' in data['player_scores']:
        data['player_scores'][new_name] = data['player_scores'].pop('Guest')
    save_scores(data)

    return redirect(url_for('game'))

@app.route('/get_player', methods=['GET'])
def get_player():
    player_name = session.get('player_name', 'Guest')
    return jsonify({'player': player_name})

if __name__ == "__main__":
    app.run(debug=True)