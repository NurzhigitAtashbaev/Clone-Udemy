from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, login_user

from . import db
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login_post():
    if request.method == 'POST':
        # login code goes here
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login_post'))  # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('app.profile'))
    return render_template('login.html')


@auth.route('/register/', methods=('GET', 'POST'))
def signup_post():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('type')
        experience = request.form.get('experience')
        audience = request.form.get('audience')
        is_mentor = request.form.get('is_mentor')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        # TODO: save the user data to a database or perform any other necessary actions

        user = User.query.filter_by(
            email=email).first()  # if this returns a user, then the email already exists in database

        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.signup_post'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.

        new_user = User(email=email,
                        password=generate_password_hash(password, method='sha256'),
                        type=user_type,
                        experience=experience,
                        audience=audience,
                        is_mentor=is_mentor,
                        first_name=first_name,
                        last_name=last_name)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login_post'))

    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app.index'))
