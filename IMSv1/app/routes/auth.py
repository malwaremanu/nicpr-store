from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = db('users')
        user = users.fetch({'email': email, 'password' : password})
        if user:
            session['user'] = user[0]
            return redirect(url_for('user.index'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))