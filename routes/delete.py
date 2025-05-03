import json
from flask import Blueprint, request, jsonify
import logging

# Získání loggeru aplikace
logger = logging.getLogger('app')

delete = Blueprint('delete', __name__)

DATA_FILE = 'data.json'  # Path to your JSON file

def load_data():
    """Loads data from the JSON file."""
    logger.info(f"Loading data from: {DATA_FILE}")
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            logger.info(f"Data loaded successfully: {data}")
            return data
    except FileNotFoundError:
        logger.warning(f"File not found: {DATA_FILE}. Returning empty dictionary.")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from: {DATA_FILE}. Returning empty dictionary.")
        return {}

def save_data(data):
    """Saves data to the JSON file."""
    logger.info(f"Saving data changes to: {DATA_FILE}")
    logger.debug(f"Data to be saved: {data}")
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)
    logger.info("Data changes saved successfully.")

@delete.route('/delete_word', methods=['POST'])
def delete_word():
    """Endpoint for deleting a word."""
    logger.info("Received request to /delete_word")
    data = load_data()  # Load the current data
    request_data = request.get_json()  # Get data from the request
    logger.debug(f"Request data: {request_data}")

    if not isinstance(request_data, dict) or 'word' not in request_data:
        logger.warning("Invalid request format. Expecting a JSON with 'word' key.")
        return jsonify({"message": "Invalid request. Please provide a JSON with the 'word' to delete."}), 400

    word_to_delete = request_data['word']

    if word_to_delete in data:
        del data[word_to_delete]  # Delete the word
        save_data(data)  # Save the changes
        logger.info(f'Word "{word_to_delete}" was successfully deleted.')
        return jsonify({"message": f'Word "{word_to_delete}" was successfully deleted.'}), 200
    else:
        logger.info(f'Word "{word_to_delete}" not found.')
        return jsonify({"message": f'Word "{word_to_delete}" not found.'}), 404