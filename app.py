from flask import Flask
from routes.game import game_bp
from routes.word import word_bp
from routes.score import score_bp
from routes.player import player_bp
from routes.game_logic import new_game, load_words
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key')  # Bezpečnější způsob pro secret key
app.config['SCORE_FILE'] = 'scores.json'
app.config['WORDS_FILE'] = 'data.json'

# Načtení slov při spuštění aplikace
app.words_with_clues = load_words(app.config['WORDS_FILE'])

# Registrace blueprintů
app.register_blueprint(game_bp)
app.register_blueprint(word_bp, url_prefix='/words')
app.register_blueprint(score_bp, url_prefix='/scores')
app.register_blueprint(player_bp, url_prefix='/player')

if __name__ == "__main__":
    app.run(debug=True)