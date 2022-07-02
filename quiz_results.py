from flask import Blueprint, render_template, request
from flask_login import login_required
from models import current_quiz

quiz_results_bp = Blueprint('quiz_results_bp', __name__)


@quiz_results_bp.route('/quiz_results', methods=["GET", "POST"])
@login_required
def quiz_results():
    quiz_id = request.form.get('quiz_id')
    quiz = current_quiz.query.filter_by(id=int(quiz_id)).first()
    return render_template("results.html", quiz_players=quiz.players)
