import json

import flask
from sqlalchemy import true

from flask_login import login_required, LoginManager, current_user

from flask import Flask, render_template, request, url_for, redirect, flash
from sqlalchemy.orm.attributes import flag_modified


from routes import main
from auth import auth
from models import Quiz, User, current_quiz
from ruhat_api import api, add_player_to_the_quiz

application = Flask(__name__)
application.config['SECRET_KEY'] = 'any-secret-key-you-choose'

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbUsers.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

application.register_blueprint(main)
application.register_blueprint(api)
application.register_blueprint(auth)

from extensions import db

db.init_app(application)
login_manager = LoginManager(application)


def json_to_dict(jsonData):
    return json.loads(jsonData)

def get_quiz_from_db(id):
    return Quiz.query.filter_by(id=id).first()

application.add_template_filter(json_to_dict)
application.add_template_filter(get_quiz_from_db)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




@application.route('/workspace', methods=["GET", "POST", "PUT", "DELETE"])
@login_required
def workspace():
    # You can see your created quizes and can create a new one
    if request.method == "POST":

        if len(request.json)==1:

            quiz_name =request.json['quiz_name']
            new_quiz = Quiz(name=quiz_name, number_of_questions=0, questions=[], opened=True)
            # Add the quiz in Quiz table
            db.session.add(new_quiz)
            db.session.commit()
            # Add the quiz in User table
            new_quiz_user= {'id':new_quiz.id,'name':new_quiz.name}
            cur_user = User.query.filter_by(id=current_user.id).first()
            list_quiz = current_user.quizzes
            list_quiz.append(new_quiz_user)
            cur_user.quizzes= list_quiz
            flag_modified(cur_user, "quizzes")
            db.session.add(cur_user)
            # db.session.merge(cur_user)
            db.session.commit()
            # print(cur_user.quizzes)
        else:
            question_text = request.json['question']
            option_A = request.json['option_A']
            option_B = request.json['option_B']
            option_C = request.json['option_C']
            option_D = request.json['option_D']
            options = [option_A,option_B,option_C,option_D]
            right_option = options[request.json['right_option']]
            new_question = {"answer": right_option, "options":options, "question" : question_text}
            quiz_id = int(request.headers.get('Referer').split('=')[-1]) # there should be another way to get the quiz_id
            quiz = Quiz.query.filter_by(id=quiz_id).first()
            quiz.number_of_questions +=1
            quiz_questions = quiz.questions
            quiz_questions.append(new_question)
            flag_modified(quiz, "questions")
            db.session.add(quiz)
            db.session.flush()
            db.session.commit()
    elif request.method == "PUT":
        state = request.json['state']
        quiz_id = int(request.headers.get('Referer').split('=')[-1])
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        quiz.opened = state
        if quiz.opened:
            running_quiz = current_quiz(quiz)
            running_quiz.owner = current_user.id
            db.session.add(running_quiz)
        else:
            quiz_for_deleting = current_quiz.query.filter_by(id=quiz_id).first()
            db.session.delete(quiz_for_deleting)
        db.session.flush()
        db.session.commit()
    elif request.method =="DELETE":

        if request.json['object_to_delete']=='question':

            quiz_id = int(request.headers.get('Referer').split('=')[-1])
            quiz = Quiz.query.filter_by(id=quiz_id).first()
            if quiz.opened:
                # if quiz is opened, we shouldn't let the teacher change it
                pass
            else:
                question_id = request.json['question']
                quiz.number_of_questions -= 1
                quiz_questions = quiz.questions
                quiz_questions.pop(question_id)
                print(quiz_questions)
                flag_modified(quiz, "questions")
                db.session.add(quiz)
                db.session.flush()
                db.session.commit()


        else:
            quiz_id = int(request.json['quiz_url'].split('=')[-1])
            quiz = Quiz.query.filter_by(id=quiz_id).first()
            db.session.delete(quiz)
            db.session.flush()
            db.session.commit()
            cur_user = User.query.filter_by(id=current_user.id).first()
            list_quiz = current_user.quizzes
            for index in range(len(list_quiz)):
                if list_quiz[index]['id']==quiz_id:
                    del list_quiz[index]
                    break
            flag_modified(cur_user, "quizzes")
            db.session.add(cur_user)
            db.session.flush()
            db.session.commit()


    quiz_list = [Quiz.query.filter_by(id=quiz_user['id']).first() for quiz_user in current_user.quizzes]
    return render_template('workspace.html', quiz_list=quiz_list)


@application.route('/quiz/<id_quiz>', methods=["GET", "POST"])
def quiz(id_quiz):

    if request.method == "POST":
        answer = list(request.form.to_dict().keys())[0]
        correct_option = Quiz.query.filter_by(id=id_quiz).first().questions[flask.session['progress']]["options"].index(
            Quiz.query.filter_by(id=id_quiz).first().questions[flask.session['progress']]['answer'])

        if answer == str(correct_option):
            quiz_taken = current_quiz.query.filter_by(id=id_quiz).first()
            quiz_players = quiz_taken.players


            for index in range(len(quiz_players)):
                if quiz_players[index]['name'] == flask.session['name']:
                    quiz_players[index]['correct_answers'] += 1
                    quiz_players[index]['current_streak'] +=1
                    quiz_players[index]['points'] += (1+(quiz_players[index]['current_streak']-1)/10)*100
                    flag_modified(quiz_taken, "players")
                    db.session.add(quiz_taken)
                    db.session.flush()
                    db.session.commit()
                    break
        else:
            quiz_taken = current_quiz.query.filter_by(id=id_quiz).first()
            quiz_players = quiz_taken.players

            for index in range(len(quiz_players)):
                if quiz_players[index]['name'] == flask.session['name']:
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

    quiz = Quiz.query.filter_by(id=id_quiz).first()
    if quiz:
        if quiz.opened:
            questions = quiz.questions
            if flask.session['progress'] == 0:
                current_player = {"name": flask.session['name'], "correct_answers": 0, "current_streak": 0, "points":0}
                add_player_to_the_quiz(current_player, quiz.id)

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
