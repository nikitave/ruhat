import flask
from flask import Blueprint, redirect, url_for, render_template
from flask import request
main = Blueprint('main', __name__)


@main.route('/invited/<id>')
@main.route('/', methods=["GET", "POST"])
def home(id=None):
    flask.session['progress'] = 0

    if request.method == "POST":
        # print(f"{request.form['username']}",file=sys.stderr)
        pincode = request.form['pincode']
        id_quiz = int(pincode)
        return redirect(url_for('quiz', id_quiz=id_quiz))
    if id:
        return render_template("startingPage.html",id=id)
    return render_template("startingPage.html")



@main.route('/')
def end_quiz():
    return 'End of the quiz'