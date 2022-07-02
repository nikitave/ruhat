from flask import Blueprint, jsonify
from flask import request
from flask_login import current_user
from sqlalchemy.orm.attributes import flag_modified
from extensions import db
from models import Quiz, current_quiz

api = Blueprint('api', __name__)


def add_player_to_the_quiz(current_player, id):
    quiz_taken = current_quiz.query.filter_by(id=id).first()
    quiz_players = quiz_taken.players
    quiz_players.append(current_player)
    flag_modified(quiz_taken, "players")
    db.session.add(quiz_taken)
    db.session.flush()
    db.session.commit()


def check_player_in_the_quiz(quiz_id, player_name):
    quiz_taken = current_quiz.query.filter_by(id=quiz_id).first()
    quiz_players = quiz_taken.players
    for player in quiz_players:
        if player['name'] == player_name:
            return True
    return False


@api.route('/api/result', methods=["GET"])
def result():
    quiz = current_quiz.query.filter_by(id=int(request.args['id'])).first()
    if quiz:
        quiz_players = quiz.players
        sorted_list_of_players = sorted(quiz_players, key=lambda d: d['points'], reverse=True)
        return jsonify(sorted_list_of_players)
    else:
        return jsonify({'status': 'Quiz is closed or does not exist'})


@api.route('/api/get_quiz', methods=["GET"])
def get_quiz():
    if 'id' in request.args:
        quiz_id = int(request.args['id'])
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if quiz:
            if quiz.opened:
                current_player = {"name": request.args['name'], "correct_answers": 0, "current_streak": 0, "points": 0}
                add_player_to_the_quiz(current_player, quiz_id)
                questions = quiz.questions
                return jsonify(questions), 200
            else:
                return jsonify({"status": "closed"}), 204
        else:
            return jsonify({"status": "not found"}), 404
    else:
        return "Error", 400


@api.route('/api/get_quizzes_from_user', methods=["GET"])
def get_quizzes_from_user():
    return jsonify(current_user.quizzes[-1])


@api.route('/api/post_answer', methods=["GET"])
def post_answer():
    quiz_taken = current_quiz.query.filter_by(id=int(request.args['id'])).first()
    quiz_players = quiz_taken.players
    for index in range(len(quiz_players)):
        if quiz_players[index]['name'] == request.args['name']:

            if request.args['correct'] == 'false':
                quiz_players[index]['current_streak'] = 0
            else:
                quiz_players[index]['correct_answers'] += 1
                quiz_players[index]['current_streak'] += 1
                quiz_players[index]['points'] += (1 + (quiz_players[index]['current_streak'] - 1) / 10) * 100
            flag_modified(quiz_taken, "players")
            db.session.add(quiz_taken)
            db.session.flush()
            db.session.commit()
            return jsonify({"status": "success"}), 200
    return jsonify({"status": "fail"}), 400


@api.route('/api/get_result', methods=["GET"])
def get_result():
    try:
        sorted_list_of_players = result().json
        print(sorted_list_of_players)
        for index in range(len(sorted_list_of_players)):
            if sorted_list_of_players[index]['name'] == request.args['name']:
                percentage = round((1 - (index / len(sorted_list_of_players))) * 100, 2)
                return jsonify(
                    {"status": "success", "points": sorted_list_of_players[index]['points'], "percentage": percentage,
                     "correct_answers": sorted_list_of_players[index]['correct_answers']}), 200
    except Exception as e:
        return jsonify({"status": "fail", "error": e}), 400
    return jsonify({"status": "fail"}), 400


@api.route('/api/get_top_5_players', methods=["GET"])
def get_top_5_players():
    quiz_taken = current_quiz.query.filter_by(id=int(request.headers.get('id'))).first()
    quiz_players = quiz_taken.players
    sorted_list_of_players = sorted(quiz_players, key=lambda d: d['points'], reverse=True)
    return jsonify(sorted_list_of_players[:5])
