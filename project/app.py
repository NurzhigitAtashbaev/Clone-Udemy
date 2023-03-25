from flask import render_template, request, url_for, redirect, Blueprint
from flask_login import login_required, current_user


app = Blueprint('app', __name__)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.email)
