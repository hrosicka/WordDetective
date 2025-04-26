from flask import Blueprint, render_template, request, current_app
import json

word_bp = Blueprint('word', __name__)

def load_words(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_words(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

@word_bp.route('/add', methods=['GET', 'POST'])
def add_word():
    message = None
    words_file = current_app.config['WORDS_FILE']
    words_data = load_words(words_file)

    if request.method == 'POST':
        word = request.form['word']
        description = request.form['description']

        if word in words_data:
            message = f"The word '{word}' already exists!"
        else:
            words_data[word] = description
            save_words(words_file, words_data)
            return render_template('add_word.html', message="Word added successfully!")

    return render_template('add_word.html', message=message)

@word_bp.route('/preview', methods=['GET'])
def preview():
    words_file = current_app.config['WORDS_FILE']
    data = load_words(words_file)
    return render_template('preview.html', data=data)