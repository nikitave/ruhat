import json
import sys
import flask
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

# from flask_mysqldb import MySQL
application = Flask(__name__)
application.config['SECRET_KEY'] = 'any-secret-key-you-choose'

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbUsers.db'

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# application.config['MYSQL_HOST'] = 'localhost'
# application.config['MYSQL_USER'] = 'u1689524_default'
# application.config['MYSQL_PASSWORD'] = '2Gir7nQJe2Z4oAnq'
# application.config['MYSQL_DB'] = 'u1689524_default'
db = SQLAlchemy(application)
login_manager = LoginManager(application)


##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    quizzes = db.Column(db.JSON)


# Structure for quizzes JSON in User class:
# quizzes = {
# { id, name }, { id, name }, ...
# }
# We need to store id for accessing the quiz from Quiz db - to get questions and answers for them
# We need to store name for showing it to the Teacher

# CREATE TABLE IN DB FOR QUIZES
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    number_of_questions = db.Column(db.Integer)
    questions = db.Column(db.JSON)


# Structure for questions:
# questions = {
# {text,answer}, {text,answer}, ...
# }

# Line below only required once, when creating DB.
# db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@application.route('/', methods=["GET", "POST"])
def home():
    flask.session['progress'] = 0
    if request.method == "POST":
        # print(f"{request.form['username']}",file=sys.stderr)
        pincode = request.form['pincode']
        id_quiz = int(pincode)
        return redirect(url_for('quiz', id_quiz=id_quiz))
    return render_template("startingPage.html")


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
            return redirect(url_for("quiz_management"))
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
                return redirect(url_for("quiz_management"))
            else:
                flash("We can't let you in until you enter the correct password.", 'login_err')
                return redirect(url_for('register', mode="sign-in-mode"))
    return render_template("index.html", mode=mode)


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@application.route('/quiz-management')
@login_required
def quiz_management():
    # You can see your created quizes and can create a new one
    return render_template('quiz_management.html')


@application.route('/quiz/<id_quiz>', methods=["GET", "POST"])
def quiz(id_quiz):
    if request.method == "POST":
        answer = request.values
        flask.session['progress'] += 1
        # print(answer)
        if flask.session['progress'] == len(Quiz.query.filter_by(id=id_quiz).first().questions):
            return redirect(url_for('home'))
    # print(flask.session['progress'])
    questions = Quiz.query.filter_by(id=id_quiz).first().questions
    return render_template('questionPage.html', question=questions[flask.session['progress']], id_quiz=id_quiz)


@application.errorhandler(500)
def page_error(e):
    return f'{e}'


if __name__ == "__main__":
    application.run()
