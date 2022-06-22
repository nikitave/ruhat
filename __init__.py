import json

import flask

from flask_login import LoginManager

from flask import Flask, render_template, request, url_for, redirect, flash
from sqlalchemy.orm.attributes import flag_modified

from extensions import db
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
def create_app():
    application = Flask(__name__)
    csrf.init_app(application)
    application.config['SECRET_KEY'] = 'any-secret-key-you-choose'
    application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbUsers.db'
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from routes import main
    from auth import auth
    from workspace import workspace_bp
    from ruhat_api import api
    application.register_blueprint(main)
    application.register_blueprint(api)
    application.register_blueprint(auth)
    application.register_blueprint(workspace_bp)
    db.init_app(application)
    return application


application = create_app()
login_manager = LoginManager(application)

from models import Quiz, User, current_quiz
from ruhat_api import add_player_to_the_quiz


def json_to_dict(json_data):
    return json.loads(json_data)


def get_quiz_from_db(id):
    return Quiz.query.filter_by(id=id).first()


application.add_template_filter(json_to_dict)
application.add_template_filter(get_quiz_from_db)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@application.route('/quiz/<id_quiz>', methods=["GET", "POST"])
def quiz(id_quiz):
    if request.method == "POST":
        answer = list(request.form.to_dict().keys())[0]
        correct_option = Quiz.query.filter_by(id=id_quiz).first().questions[flask.session['progress']]["options"].index(
            Quiz.query.filter_by(id=id_quiz).first().questions[flask.session['progress']]['answer'])
        quiz_taken = current_quiz.query.filter_by(id=id_quiz).first()
        quiz_players = quiz_taken.players
        for index in range(len(quiz_players)):
            if quiz_players[index]['name'] == flask.session['name']:
                if answer == str(correct_option):
                    quiz_players[index]['correct_answers'] += 1
                    quiz_players[index]['current_streak'] += 1
                    quiz_players[index]['points'] += (1 + (quiz_players[index]['current_streak'] - 1) / 10) * 100
                else:
                    quiz_players[index]['current_streak'] = 0
                flag_modified(quiz_taken, "players")
                db.session.add(quiz_taken)
                db.session.flush()
                db.session.commit()
                break
        flask.session['progress'] += 1
        if int(flask.session['progress']) == len(Quiz.query.filter_by(id=id_quiz).first().questions):
            quiz_taken = current_quiz.query.filter_by(id=id_quiz).first()
            quiz_players = quiz_taken.players
            for index in range(len(quiz_players)):
                if quiz_players[index]['name'] == flask.session['name']:
                    flask.session['count'] = quiz_players[index]['correct_answers']
                    flask.session['points'] = quiz_players[index]['points']
                    return redirect(url_for('main.end_quiz'))

        else:
            return redirect(url_for('quiz', id_quiz=id_quiz))

    quiz_taken = Quiz.query.filter_by(id=id_quiz).first()
    if quiz_taken:
        if quiz.taken:
            questions = quiz.questions
            if flask.session['progress'] == 0:
                current_player = {"name": flask.session['name'], "correct_answers": 0, "current_streak": 0, "points": 0}
                add_player_to_the_quiz(current_player, quiz_taken.id)

            return render_template('questionPage.html', question=questions[flask.session['progress']], id_quiz=id_quiz)
        else:
            flash("The quiz is closed.")
    else:
        flash("The quiz does not exist.")
    return redirect(url_for('main.home'))


@application.errorhandler(404)
def not_existed_page(e):
    return '''This page doesn't exist. Please, leave this page immediately.'''


application.register_error_handler(404, not_existed_page)

if __name__ == "__main__":
    application.run(debug=True)
