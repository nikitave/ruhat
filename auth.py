
from flask import Blueprint, redirect, url_for, render_template, flash
from flask import request
from flask_login import logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from extensions import *
auth = Blueprint('auth', __name__)



@auth.route('/register/<mode>', methods=["GET", "POST"])
def register(mode):
    if request.method == "POST":
        # if request.form has 3 elements in it (password,email,username),
        # an user tries to register
        # otherwise the user tries to log in
        if len(request.form) == 3:
            # if user already exists, flash them a message
            if User.query.filter_by(email=request.form['email']).first():
                flash("We have found your email in our database, try to log in.", 'reg_err')
                return redirect(url_for('auth.register', mode=mode))
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
                return redirect(url_for('auth.register', mode="sign-in-mode"))
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("workspace"))
            else:
                flash("We can't let you in until you enter the correct password.", 'login_err')
                return redirect(url_for('auth.register', mode="sign-in-mode"))
    return render_template("index.html", mode=mode)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))
