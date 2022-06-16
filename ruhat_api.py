# import flask
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


@api.route('/api/get_quiz', methods=["GET"])
def get_questions():
    if 'id' in request.args:
        id = int(request.args['id'])
        quiz = Quiz.query.filter_by(id=id).first()
        if quiz:
            if quiz.opened:
                current_player = {"name": request.args['name'], "correct_answers": 0}
                add_player_to_the_quiz(current_player, id)
                questions = quiz.questions
                return jsonify(questions),200
            else:
                return jsonify({"status":"closed"}),204
        else:
            return jsonify({"status":"not found"}),404
    else:
        return "Error",400

@api.route('/api/get_quizzes_from_user', methods=["GET"])
def get_quizzes_from_user():
    return jsonify(current_user.quizzes[-1])


@api.route('/api/post_answer', methods=["GET"])
def post_answer():
    if 'option' in request.args:
        pass
        # request.args['option']
        # TODO: To link the user of the api with the database
    return "Error"
