import json
import flask
from extensions import db
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import LoginManager
from models import Quiz, User, current_quiz
from ruhat_api import add_player_to_the_quiz, check_player_in_the_quiz
from sqlalchemy.orm.attributes import flag_modified

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "any-secret-key-you-choose"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dbUsers.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    from auth import auth
    from routes import main
    from ruhat_api import api
    from workspace import workspace_bp

    app.register_blueprint(main)
    app.register_blueprint(api)
    app.register_blueprint(auth)
    app.register_blueprint(workspace_bp)
    db.init_app(app)
    return app


application = create_app()
login_manager = LoginManager(application)


def json_to_dict(json_data):
    return json.loads(json_data)


def get_quiz_from_db(quiz_id):
    return Quiz.query.filter_by(id=quiz_id).first()


application.add_template_filter(json_to_dict)
application.add_template_filter(get_quiz_from_db)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@application.route("/quiz/<quiz_id>", methods=["GET", "POST"])
def quiz(quiz_id):
    if request.method == "POST":
        answer = list(request.form.to_dict().keys())[0]
        correct_option = (
            Quiz.query.filter_by(id=quiz_id)
            .first()
            .questions[flask.session["progress"]]["options"]
            .index(
                Quiz.query.filter_by(id=quiz_id)
                .first()
                .questions[flask.session["progress"]]["answer"]
            )
        )
        quiz_taken = current_quiz.query.filter_by(id=quiz_id).first()
        quiz_players = quiz_taken.players
        for index in range(len(quiz_players)):
            if quiz_players[index]["name"] == flask.session["name"]:
                if answer == str(correct_option):
                    quiz_players[index]["correct_answers"] += 1
                    quiz_players[index]["current_streak"] += 1
                    quiz_players[index]["points"] += (1 + (quiz_players[index]["current_streak"] - 1) / 10) * 100
                else:
                    quiz_players[index]["current_streak"] = 0
                flag_modified(quiz_taken, "players")
                db.session.add(quiz_taken)
                db.session.flush()
                db.session.commit()
                break
        flask.session["progress"] += 1
        if int(flask.session["progress"]) == len(
                Quiz.query.filter_by(id=quiz_id).first().questions
        ):
            quiz_taken = current_quiz.query.filter_by(id=quiz_id).first()
            quiz_players = quiz_taken.players
            for index in range(len(quiz_players)):
                if quiz_players[index]["name"] == flask.session["name"]:
                    flask.session["count"] = quiz_players[index]["correct_answers"]
                    flask.session["points"] = quiz_players[index]["points"]
                    return redirect(url_for("main.end_quiz"))

        else:
            return redirect(url_for("quiz", quiz_id=quiz_id))

    quiz_taken = Quiz.query.filter_by(id=quiz_id).first()
    if quiz_taken:
        if quiz_taken.opened:
            questions = quiz_taken.questions
            if flask.session["progress"] == 0:
                current_player = {
                    "name": flask.session["name"],
                    "correct_answers": 0,
                    "current_streak": 0,
                    "points": 0,
                }
                if check_player_in_the_quiz(quiz_id, current_player["name"]):
                    return redirect(url_for("main.home"))
                add_player_to_the_quiz(current_player, quiz_taken.id)

            return render_template("questionPage.html", question=questions[flask.session["progress"]], quiz_id=quiz_id)
        else:
            flash("The quiz is closed")
    else:
        flash("The quiz does not exist.")
    return redirect(url_for("main.home"))


@application.errorhandler(404)
def not_existed_page(error):
    return """This page doesn't exist. Please, leave this page immediately."""


application.register_error_handler(404, not_existed_page)

if __name__ == "__main__":
    application.run(debug=True)
