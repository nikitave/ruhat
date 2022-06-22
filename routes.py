import flask
from flask import Blueprint, redirect, url_for, render_template, current_app
from flask import request

main = Blueprint('main', __name__)


@main.route('/invited/<id>')
@main.route('/', methods=["GET", "POST"])
def home(id=None):
    current_app.logger.info("Home page")
    flask.session['progress'] = 0
    if "_flashes" not in dict(flask.session.items()):
        flask.session['name'] = ''
    if request.method == "POST":
        pincode = request.form['pincode']
        id_quiz = int(pincode)
        user_name = request.form['username']
        flask.session['name'] = user_name
        return redirect(url_for('quiz', id_quiz=id_quiz))
    if id:
        return render_template("startingPage.html", id=id)
    return render_template("startingPage.html", name=flask.session['name'])


@main.route('/end_quiz')
def end_quiz():
    return render_template("resultUserPage.html", count=flask.session['count'], points=int(flask.session['points']))
