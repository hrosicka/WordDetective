from flask import Flask
from routes.game import game_bp
from routes.word import word_bp
from routes.score import score_bp
from routes.player import player_bp
from routes.game_logic import load_words
import os
import json  # Import the json module for potential JSON parsing exceptions
import logging

class Config:
    """Configuration class to encapsulate application settings."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    SCORE_FILE = 'scores.json'
    WORDS_FILE = 'data.json'
    LOG_FILE = 'app.log'

app = Flask(__name__)
app.config.from_object(Config)

# Logging Configuration
def configure_logging():
    """Configure logging for the application."""
    log_file = app.config['LOG_FILE']

    # Create a logger for the application
    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)  # Set the logger's level to INFO

    # Create file handler to log to file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)  # Set the file handler's level to INFO

    # Create console handler to log to console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)  # Set the stream handler's level to INFO

    # Define a common log format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # Attach the configured logger to the Flask app
    app.logger.handlers = []  # Remove default handlers
    app.logger.propagate = False  # Prevent propagation to the root logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)

# Apply logging configuration
configure_logging()

# Attempt to load game words and their associated clues upon application initialization.
# This ensures that the word data is readily available for gameplay.
try:
    app.words_with_clues = load_words(app.config['WORDS_FILE'])
    app.logger.info(f"Words and clues successfully loaded from '{app.config['WORDS_FILE']}'.")
except FileNotFoundError:
    app.logger.error(f"The word data file '{app.config['WORDS_FILE']}' was not found.")
    app.words_with_clues = {}  # Initialize an empty dictionary to allow the application to start gracefully, albeit without word data.
except json.JSONDecodeError:
    app.logger.error(f"The word data file '{app.config['WORDS_FILE']}' contains invalid JSON format.")
    app.words_with_clues = {}  # Initialize an empty dictionary to prevent application startup failure due to malformed data.
except Exception as e:
    app.logger.exception(f"An unexpected error occurred during the loading of word data: {e}")
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