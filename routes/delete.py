import json
from flask import Blueprint, request, jsonify

delete = Blueprint('delete', __name__)

DATA_FILE = 'data.json'  # Cesta k vašemu JSON souboru

def load_data():
    """Načte data ze souboru JSON."""
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    """Uloží data do souboru JSON."""
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@delete.route('/delete_word', methods=['POST'])
def delete_word():
    """Endpoint pro mazání slova."""
    data = load_data()  # Načtení aktuálních dat
    request_data = request.get_json()  # Získání dat z požadavku
    word_to_delete = request_data.get('word')

    if word_to_delete in data:
        del data[word_to_delete]  # Smazání slova
        save_data(data)  # Uložení změn
        return jsonify({"message": f'Word "{word_to_delete}" was successfully deleted.'}), 200
    else:
        return jsonify({"message": f'Word "{word_to_delete}" not found.'}), 404