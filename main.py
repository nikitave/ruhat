import json

import flask
import werkzeug.exceptions
from flask import Flask, render_template, request, url_for, redirect
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
import auth


# from flask_mysqldb import MySQL
application = Flask(__name__)
application.config['SECRET_KEY'] = 'any-secret-key-you-choose'

# application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbUsers.db'
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://u1689524_default:2Gir7nQJe2Z4oAnq@37.140.192.174:3306/u1689524_default'

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)



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
    opened = db.Column(db.Boolean)

# Structure for questions:
# questions = {
# {text,answer}, {text,answer}, ...
# }

# Line below only required once, when creating DB.
# db.create_all()


def json_to_dict(jsonData):
    return json.loads(jsonData)

application.add_template_filter(json_to_dict)



@application.route('/', methods=["GET", "POST"])
def home():
    flask.session['progress'] = 0
    if request.method == "POST":
        # print(f"{request.form['username']}",file=sys.stderr)
        pincode = request.form['pincode']
        id_quiz = int(pincode)
        return redirect(url_for('quiz', id_quiz=id_quiz))
    return render_template("startingPage.html")


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
            return redirect(url_for('home'))
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
