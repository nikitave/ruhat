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
