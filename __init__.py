import json

import flask
import werkzeug

from flask_login import login_required, login_user, logout_user, LoginManager, current_user

from flask import Flask, render_template, request, url_for, redirect, flash, jsonify

from werkzeug.security import generate_password_hash, check_password_hash

from routes import main
from models import Quiz, User

application = Flask(__name__)
application.config['SECRET_KEY'] = 'any-secret-key-you-choose'

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbUsers.db'

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

application.register_blueprint(main)

from extensions import db

db.init_app(application)
login_manager = LoginManager(application)


def json_to_dict(jsonData):
    return json.loads(jsonData)


application.add_template_filter(json_to_dict)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@application.route('/register/<mode>', methods=["GET", "POST"])
def register(mode):
    if request.method == "POST":
        # if request.form has 3 elements in it (password,email,username),
        # an user tries to register
        # otherwise the user tries to log in
        if len(request.form) == 3:
            # if user already exists, flash them a message
            if User.query.filter_by(email=request.form['email']).first():
                flash("We have found your email in our database, try to log in.", 'reg_err')
                return redirect(url_for('register', mode=mode))
            hash_and_salted_password = generate_password_hash(
                request.form['password'],
                method='pbkdf2:sha256',
                salt_length=8
            )
            new_user = User(
                email=request.form['email'],
                name=request.form['username'],
                password=hash_and_salted_password,
            )

            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("workspace"))
        else:
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if not user:
                flash("We can't find your email in our database, please try again.", 'login_err')
                # print(request.form, file=sys.stderr)
                return redirect(url_for('register', mode="sign-in-mode"))
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("workspace"))
            else:
                flash("We can't let you in until you enter the correct password.", 'login_err')
                return redirect(url_for('register', mode="sign-in-mode"))
    return render_template("index.html", mode=mode)


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@application.route('/workspace', methods=["GET", "POST"])
@login_required
def workspace():
    # You can see your created quizes and can create a new one
    if request.method == "POST":
        print(request.values)
    else:
        quiz_list = [Quiz.query.filter_by(id=quiz_user['id']).first() for quiz_user in current_user.quizzes]
    return render_template('workspace.html', quiz_list=quiz_list)


@application.route('/quiz/<id_quiz>', methods=["GET", "POST"])
def quiz(id_quiz):

    if request.method == "POST":
        answer = request.values
        flask.session['progress'] += 1
        # TODO: to link the user with the database and store his answers and his score in the database
        # print(answer)
        if int(flask.session['progress']) == len(Quiz.query.filter_by(id=id_quiz).first().questions):
            return redirect(url_for('main.end_quiz'))

    quiz = Quiz.query.filter_by(id=id_quiz).first()
    if quiz:
        if quiz.opened:
            questions = quiz.questions
            return render_template('questionPage.html', question=questions[flask.session['progress']], id_quiz=id_quiz)
        else:
            return 'Quiz is closed'
    else:
        raise NotExistingQuiz()




@application.route('/api/get_quiz', methods=["GET"])
def get_questions():
    if 'id' in request.args:
        id = int(request.args['id'])
        quiz = Quiz.query.filter_by(id=id).first()
        if quiz:
            if quiz.opened:
                questions = quiz.questions
                return jsonify(questions),200
            else:
                return jsonify({"status":"closed"}),204
        else:
            return jsonify({"status":"not found"}),404
    else:
        return "Error",400

@application.route('/api/post_answer', methods=["GET"])
def post_answer():
    if 'option' in request.args:
        pass
        # request.args['option']
        # TODO: To link the user of the api with the database
    return "Errro"

@application.errorhandler(404)
def not_existed_page(e):
    return '''This page doesn't exist. Please, leave this page immediately.'''


application.register_error_handler(404, not_existed_page)


class NotExistingQuiz(werkzeug.exceptions.HTTPException):
    code = 4040
    description = "This quiz doesn't exist"


@application.errorhandler(NotExistingQuiz)
def page_error(e):
    return f'{e.description}'


application.register_error_handler(NotExistingQuiz, page_error)
if __name__ == "__main__":
    application.run(debug=True)
