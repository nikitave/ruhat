from flask import Blueprint, render_template, flash, redirect, url_for
from flask import request
from flask_login import login_required, current_user
from sqlalchemy.orm.attributes import flag_modified

from models import Quiz, current_quiz, User
from extensions import db

workspace_bp = Blueprint('workspace_bp', __name__)


@workspace_bp.route('/workspace', methods=["GET", "POST", "PUT", "DELETE"])
@login_required
def workspace():
    if request.method == "POST":
        if len(request.json) == 1:

            quiz_name = request.json['quiz_name']
            new_quiz = Quiz(name=quiz_name, number_of_questions=0, questions=[], opened=False)
            # Add the quiz in Quiz table
            db.session.add(new_quiz)
            db.session.commit()
            # Add the quiz in User table
            new_quiz_user = {'id': new_quiz.id, 'name': new_quiz.name}
            cur_user = User.query.filter_by(id=current_user.id).first()
            list_quiz = current_user.quizzes
            list_quiz.append(new_quiz_user)
            cur_user.quizzes = list_quiz
            flag_modified(cur_user, "quizzes")
            db.session.add(cur_user)
            db.session.commit()
        else:
            question_text = request.json['question']
            options = [request.json['option_A'],
                       request.json['option_B'],
                       request.json['option_C'],
                       request.json['option_D']]
            right_option = options[request.json['right_option']]
            new_question = {"answer": right_option, "options": options, "question": question_text}
            quiz_id = int(request.headers.get('Referer').split('=')[-1])
            quiz = Quiz.query.filter_by(id=quiz_id).first()
            quiz.number_of_questions += 1
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
    elif request.method == "DELETE":
        if request.json['object_to_delete'] == 'question':
            quiz_id = int(request.headers.get('Referer').split('=')[-1])
            quiz = Quiz.query.filter_by(id=quiz_id).first()
            if quiz.opened:
                flash('You can\'t delete a question while the quiz is running!')
                return redirect(url_for('workspace_bp.workspace'))
                # there should be a message that informs an user that the quiz cannot be changed while it's opened
            else:
                question = request.json['question']
                question_text = question.strip()
                quiz.number_of_questions -= 1
                quiz_questions = quiz.questions
                question_entry = list(filter(lambda quest: quest['question'] == question_text, quiz_questions))[0]
                question_id = quiz_questions.index(question_entry)
                quiz_questions.pop(question_id)
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
                if list_quiz[index]['id'] == quiz_id:
                    del list_quiz[index]
                    break
            flag_modified(cur_user, "quizzes")
            db.session.add(cur_user)
            db.session.flush()
            db.session.commit()

    quiz_list = [Quiz.query.filter_by(id=quiz_user['id']).first() for quiz_user in current_user.quizzes]
    return render_template('workspace.html', quiz_list=quiz_list)
