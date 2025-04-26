from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, current_app
import json

player_bp = Blueprint('player', __name__, url_prefix='/player')

def load_scores(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"player_scores": {}}
    except json.JSONDecodeError:
        return {"player_scores": {}}

def save_scores(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

@player_bp.route('/change_name', methods=['GET', 'POST'])
def change_name():
    scores_file = current_app.config['SCORE_FILE']
    if request.method == 'POST':
        selected_player = request.form.get('selected_player')
        new_player_name = request.form.get('new_player_name')

        session['player_name'] = new_player_name if new_player_name else selected_player
        session['word_guessed'] = False
        return redirect(url_for('game.game'))

    scores = load_scores(scores_file)
    return render_template('change_name.html', players=scores['player_scores'])

@player_bp.route('/update_name', methods=['POST'])
def update_name():
    scores_file = current_app.config['SCORE_FILE']
    new_name = request.form.get('player_name', 'Guest')
    session['player_name'] = new_name

    data = load_scores(scores_file)
    if 'Guest' in data['player_scores']:
        data['player_scores'][new_name] = data['player_scores'].pop('Guest')
    save_scores(scores_file, data)

    return redirect(url_for('game.game'))

@player_bp.route('/get', methods=['GET'])
def get_player():
    player_name = session.get('player_name', 'Guest')
    return jsonify({'player': player_name})