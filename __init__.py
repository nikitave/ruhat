import json

import flask
from sqlalchemy import true
import werkzeug

from flask_login import login_required, login_user, logout_user, LoginManager, current_user

from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from sqlalchemy.orm.attributes import flag_modified

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

def get_quiz_from_db(id):
    return Quiz.query.filter_by(id=id).first()

application.add_template_filter(json_to_dict)
application.add_template_filter(get_quiz_from_db)

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
                quizzes=[]
            )

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
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
        db.session.flush()
        db.session.commit()
    elif request.method =="DELETE":
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
    return render_template('workspace.html', quiz_list=quiz_list, quiz_for_edit=None)


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

@application.route('/api/get_quizzes_from_user', methods=["GET"])
def get_quizzes_from_user():
    print(current_user.quizzes)
    return jsonify(current_user.quizzes[-1])


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
    application.run(debug=true)
