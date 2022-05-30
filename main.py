
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

application = Flask(__name__)
application.config['SECRET_KEY'] = 'any-secret-key-you-choose'

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)
login_manager = LoginManager(application)


##CREATE TABLE IN DB
class user(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    quizzes = db.Column(db.JSON)


@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))


# Structure for quizzes JSON in User class:
# quizzes = {
# { id, name }, { id, name }, ...
# }
# We need to store id for accessing the quiz from Quiz db - to get questions and answers for them
# We need to store name for showing it to the Teacher

##CREATE TABLE IN DB FOR QUIZES
# class quiz(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     name = db.Column(db.Sgot tring(100))
#     questions = db.Column(db.JSON)
#       number_of_questions =...

# Structure for questions:
# questions = {
# {text,options,answer}, {text,answer}, ...
# }



@application.route('/')
def home():
    return render_template("startingPage.html")


@application.route('/register/<mode>', methods=["GET", "POST"])
def register(mode):
    if request.method == "POST":
        # if request.form has 3 elements in it (password,email,username),
        # an user tries to register
        # otherwise the user tries to log in
        if len(request.form) == 3:
            # if user already exists, flash them a message
            if user.query.filter_by(email=request.form['email']).first():
                flash("We have found your email in our database, try to log in.", 'reg_err')
                return redirect(url_for('register', mode=mode))
            hash_and_salted_password = generate_password_hash(
                request.form['password'],
                method='pbkdf2:sha256',
                salt_length=8
            )
            new_user = user(
                email=request.form['email'],
                name=request.form['username'],
                password=hash_and_salted_password,
            )

            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("quiz_management"))
        else:
            email = request.form.get('email')
            password = request.form.get('password')
            User = user.query.filter_by(email=email).first()
            if not User:
                flash("We can't find your email in our database, please try again.", 'login_err')
                # print(request.form, file=sys.stderr)
                return redirect(url_for('register', mode="sign-in-mode"))
            if check_password_hash(User.password, password):
                login_user(User)
                return redirect(url_for("quiz_management"))
            else:
                flash("We can't let you in until you enter the correct password.", 'login_err')
                return redirect(url_for('register', mode="sign-inmode"))
    return render_template("index.html", mode=mode)


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@application.route('/quiz-management')
@login_required
def quiz_management():
    # You can see your created quizes and can create a new one
    return render_template('quiz_management.html')


if __name__ == "__main__":
    application.run()
