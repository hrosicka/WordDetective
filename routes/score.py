from flask import Blueprint, jsonify, session, current_app, render_template
import json

score_bp = Blueprint('score', __name__)

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

@score_bp.route('/update', methods=['POST'])
def update_score(points=None):
    if points is None:
        try:
            points = int(request.form.get('points', 0))
        except ValueError:
            return jsonify({"error": "Invalid points value"}), 400

    scores_file = current_app.config['SCORE_FILE']
    data = load_scores(scores_file)
    scores = data["player_scores"]
    player = session.get('player_name', 'Guest')

    if player in scores:
        scores[player] += points
    else:
        scores[player] = points

    save_scores(scores_file, data)
    return jsonify({"message": f"Updated score for {player}", "scores": scores})

@score_bp.route('/', methods=['GET'])
def get_scores():
    scores_file = current_app.config['SCORE_FILE']
    data = load_scores(scores_file)
    player = session.get('player_name', 'Guest')
    score = data["player_scores"].get(player, 0)
    return jsonify({"player": player, "score": score})

@score_bp.route('/leaderboard', methods=['GET'])
def leaderboard():
    scores_file = current_app.config['SCORE_FILE']
    data = load_scores(scores_file)
    sorted_scores = sorted(data["player_scores"].items(), key=lambda x: x[1], reverse=True)
    return render_template('leaderboard.html', leaderboard=sorted_scores)