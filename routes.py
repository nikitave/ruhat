import flask
from flask import Blueprint, redirect, url_for, render_template
from flask import request
main = Blueprint('main', __name__)



@main.route('/', methods=["GET", "POST"])
def home():
    flask.session['progress'] = 0
    if request.method == "POST":
        # print(f"{request.form['username']}",file=sys.stderr)
        pincode = request.form['pincode']
        id_quiz = int(pincode)
        return redirect(url_for('quiz', id_quiz=id_quiz))
    return render_template("startingPage.html")
