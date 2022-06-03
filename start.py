#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, flash, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, DataRequired

## Define the flask app.
app = Flask(__name__)

## Database section
# Database settings
db_uri = 'sqlite:///data/project.db'
app.config.update(
        SECRET_KEY = 'topsecret',
        SQLALCHEMY_DATABASE_URI = db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        )
db = SQLAlchemy(app)

# Flask-login's user database.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))

# Create the databse and default user if it doesn't exist. 
if not database_exists(db_uri):
    db.create_all()
    user = User(username='admin',email='admin@example.com',password=generate_password_hash('admin', method='sha256'))
    db.session.add(user)
    db.session.commit()


## Flask-login's settings
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def get(id):
    return User.query.get(id)


## Flask WTForms
class LoginForm(FlaskForm):
    username = StringField('Username :', validators=[DataRequired()])
    password = PasswordField('Password :', validators=[DataRequired()])
    submit = SubmitField('Sign In')


## Flask routes
@app.route("/", methods=['GET'])
def default():
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        session['url'] = url_for('default')
        return redirect('/login')

@app.route("/profile", methods=['GET'])
def profile():
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        return render_template('profile.html', name=current_user.username, id=user.id, user=user.username, email=user.email)
    else:
        session['url'] = url_for('profile')
        return redirect('/login')

@app.route("/profile", methods=['POST'])
@login_required
def profile_post():
    return redirect(url_for('profile'))

@app.route("/about/")
def about():
    if current_user.is_authenticated:
        return render_template('about.html')
    else:
        session['url'] = url_for('about')
        return redirect('/login')

@app.route("/login", methods=['GET'])
def login_get():
    if current_user.is_authenticated:
        return redirect('/')
    else:
        form = LoginForm()
        return render_template('login2.html', form=form)

@app.route("/login", methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        flash('Check your login details and try again.')
        return redirect('/login')
    login_user(user)
    if 'url' in session:
        return redirect(session['url'])
    else:
        return redirect('/')
    
@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    return redirect('/login')


## Launch the app using Flask's built-in server. 
if __name__ == '__main__':
    # Start with flask server
    app.run(debug=True)