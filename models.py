from flask import jsonify
from flask_login import UserMixin


from extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    quizzes = db.Column(db.JSON)
    def __init__(self,email,password,name,quizzes):
        self.name = name
        self.email = email
        self.password = password
        self.quizzes = quizzes




class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    number_of_questions = db.Column(db.Integer)
    questions = db.Column(db.JSON)
    opened = db.Column(db.Boolean)


class current_quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    players = db.Column(db.JSON)
    owner = db.Column(db.Integer)
    def __init__(self, quiz):
        self.id = quiz.id
        self.name = quiz.name
        self.players = []



# Structure for quizzes JSON in User class:
# quizzes = {
# { id, name }, { id, name }, ...
# }
# We need to store id for accessing the quiz from Quiz db - to get questions and answers for them
# We need to store name for showing it to the Teacher

# Structure for questions in Quiz class:
# questions = {
# {answer, options, question}, ...
# }

# Structure for current_quizzes:
# (id, name) as usual
# players - json: [{student_name, student_points},{...},... ]
# owner - id of a teacher from USER table