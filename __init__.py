import json

import flask
import werkzeug

from flask_login import login_required, login_user, logout_user, LoginManager

from flask import Flask, render_template, request, url_for, redirect, flash

from werkzeug.security import generate_password_hash, check_password_hash

# from extensions import db
from routes import main
from models import Quiz, User

# from flask_mysqldb import MySQL
application = Flask(__name__)
application.config['SECRET_KEY'] = 'any-secret-key-you-choose'

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbUsers.db'

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

application.register_blueprint(main)
from flask_login import UserMixin

from extensions import db


db.init_app(application)
# db.create_all()
login_manager = LoginManager(application)

# Structure for quizzes JSON in User class:
# quizzes = {
# { id, name }, { id, name }, ...
# }
# We need to store id for accessing the quiz from Quiz db - to get questions and answers for them
# We need to store name for showing it to the Teacher

# CREATE TABLE IN DB FOR QUIZES

# Structure for questions:
# questions = {
# {text,answer}, {text,answer}, ...
# }

# Line below only required once, when creating DB.
# db.create_all()


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
    return redirect(url_for('home'))







@application.route('/workspace')
@login_required
def workspace():
    # You can see your created quizes and can create a new one
    return render_template('workspace.html')


@application.route('/quiz/<id_quiz>', methods=["GET", "POST"])
def quiz(id_quiz):

    if request.method == "POST":
        answer = request.values
        flask.session['progress'] += 1
        # print(answer)
        if flask.session['progress'] == len(Quiz.query.filter_by(id=id_quiz).first().questions):
            return redirect(url_for('main.home'))
    # print(flask.session['progress'])
    quiz =  Quiz.query.filter_by(id=id_quiz).first()
    if quiz:
        if quiz.opened:
            questions = quiz.questions
            return render_template('questionPage.html', question=questions[flask.session['progress']], id_quiz=id_quiz)
        else:
            return 'Quiz is closed'
    else:
        raise NotExistingQuiz()



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
    application.run()
