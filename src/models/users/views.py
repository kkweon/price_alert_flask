from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.utils import redirect

import src.models.users.decorators as user_decorators
from src.models.users.errors import UserError
from src.models.users.user import User

user_blueprint = Blueprint("users", __name__)


@user_blueprint.route("/login", methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('.user_alerts'))

        except UserError as e:
            return e.message

    return render_template('users/login.html')


@user_blueprint.route("/register", methods=['GET', 'POST'])
def register_user():
    if session['email']:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for('.user_alerts'))

        except UserError as e:
            return e.message

    return render_template('users/register.html')


@user_blueprint.route("/alerts")
@user_decorators.requires_login
def user_alerts():
    user = User.find_by_email(session['email'])
    alerts = user.get_alerts()

    return render_template('users/alerts.html', alerts=alerts)


@user_blueprint.route("/logout")
def logout_user():
    session['email'] = None

    return redirect(url_for('home'))


@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass
