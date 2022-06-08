from flask_login import UserMixin

from extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    quizzes = db.Column(db.JSON)



class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    number_of_questions = db.Column(db.Integer)
    questions = db.Column(db.JSON)
    opened = db.Column(db.Boolean)


class Current_quizzes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    players = db.Column(db.JSON)
    owner = db.Column(db.Integer)


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