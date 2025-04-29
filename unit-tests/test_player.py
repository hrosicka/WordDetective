# GameWebWord Hunt> python -m unittest unit-tests/test_player.py

import unittest
import json
from pathlib import Path
from routes.player import load_scores, save_scores, player_bp  # Předpokládám, že player.py je v balíčku your_package_name
from routes.game import game_bp
from flask import Flask
from flask.testing import FlaskClient

class TestPlayerFunctions(unittest.TestCase):

    def setUp(self):
        """Nastavení před každým testem."""
        self.app = Flask(__name__)
        self.app.config['SCORE_FILE'] = 'test_scores.json'  # Použijeme dočasný soubor pro testování
        self.app.config['SECRET_KEY'] = 'your_secret_key'
        self.app.words_with_clues = [{"word": "test", "clues": ["clue1"]}] 
        self.app.register_blueprint(game_bp)
        self.app.register_blueprint(player_bp)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Úklid po každém testu."""
        Path('test_scores.json').unlink(missing_ok=True)
        Path('test_save.json').unlink(missing_ok=True)
        Path('invalid.json').unlink(missing_ok=True)
        Path('test_update_guest.json').unlink(missing_ok=True)
        Path('test_update_no_guest.json').unlink(missing_ok=True)
        self.app_context.pop()

    def test_load_scores_existing_file(self):
        # Define the test data representing player scores
        test_data = {"player_scores": {"Alice": 100, "Bob": 50}}
        # Open a file named 'test_scores.json' in write mode ('w')
        with open('test_scores.json', 'w') as f:
            # Dump the test_data into the file as JSON
            json.dump(test_data, f)
        # Call the load_scores function with the path to the created file
        scores = load_scores('test_scores.json')
        # Assert that the scores loaded from the file are equal to the original test_data
        self.assertEqual(scores, test_data)

    def test_load_scores_non_existing_file(self):
        # Call the load_scores function with a path to a non-existent file
        scores = load_scores('non_existent.json')
        # Assert that the function returns the expected default dictionary for a non-existent file
        self.assertEqual(scores, {"player_scores": {}})

    def test_load_scores_invalid_json(self):
        # Open a file named 'invalid.json' in write mode ('w')
        with open('invalid.json', 'w') as f:
            # Write a string that is not valid JSON to the file
            f.write('not a json')
        # Call the load_scores function with the path to the file containing invalid JSON
        scores = load_scores('invalid.json')
        # Assert that the function returns the expected default dictionary when the JSON is invalid
        self.assertEqual(scores, {"player_scores": {}})

if __name__ == '__main__':
    unittest.main()