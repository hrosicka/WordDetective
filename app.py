from flask import Flask
from routes.game import game_bp
from routes.word import word_bp
from routes.score import score_bp
from routes.player import player_bp
from routes.game_logic import load_words
import os
import json  # Import the json module for potential JSON parsing exceptions

class Config:
    """Configuration class to encapsulate application settings."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    SCORE_FILE = 'scores.json'
    WORDS_FILE = 'data.json'

app = Flask(__name__)
app.config.from_object(Config)

# Attempt to load game words and their associated clues upon application initialization.
# This ensures that the word data is readily available for gameplay.
try:
    app.words_with_clues = load_words(app.config['WORDS_FILE'])
except FileNotFoundError:
    print(f"Error: The word data file '{app.config['WORDS_FILE']}' was not found.")
    app.words_with_clues = {}  # Initialize an empty dictionary to allow the application to start gracefully, albeit without word data.
except json.JSONDecodeError:
    print(f"Error: The word data file '{app.config['WORDS_FILE']}' contains invalid JSON format.")
    app.words_with_clues = {}  # Initialize an empty dictionary to prevent application startup failure due to malformed data.
except Exception as e:
    print(f"An unexpected error occurred during the loading of word data: {e}")
    app.words_with_clues = {}  # As a fallback, initialize an empty dictionary to ensure the application can proceed.

# Register blueprints to modularize the application's routes and functionality.
# Each blueprint handles a specific set of related routes.
app.register_blueprint(game_bp)
app.register_blueprint(word_bp, url_prefix='/words')  # Mount the word blueprint under the '/words' prefix.
app.register_blueprint(score_bp, url_prefix='/scores') # Mount the score blueprint under the '/scores' prefix.
app.register_blueprint(player_bp, url_prefix='/player') # Mount the player blueprint under the '/player' prefix.

if __name__ == "__main__":
    # Run the Flask development server. Enabling debug mode facilitates development by providing
    # automatic reloading upon code changes and a more detailed error reporting interface.
    app.run(debug=True)