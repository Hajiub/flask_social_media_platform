from . import auth
from flask import session, request, url_for, render_template, redirect, abort, flash, current_app
from app.forms import SigninForm, LoginForm
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
import os
from app import csrf
from .utils import MakeFolder

@auth.route('/signin', methods=['POST', 'GET'])
@csrf.exempt
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SigninForm()
    if form.validate_on_submit():
        user = User(
                first_name = form.data.get('first_name'),
                last_name  = form.data.get('last_name'),
                email      = form.data.get('email'),
                password   = generate_password_hash(form.data.get('password1'), 'sha256'),
                birthday   = form.data.get('birthday'),
        )
        try:
            db.session.add(user)
            db.session.commit()
            user_dep = MakeFolder(current_app, user=user)
            user_dep.make_folder()
        except Exception as e:
            flash('Something went wrong. Please try again! Error: ' + str(e))
            return redirect(url_for('auth.signin'))
        return redirect(url_for('auth.login'))
    return render_template('auth/signin.html', form=form)

@auth.route('/login', methods=['POST', 'GET'])
@csrf.exempt
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form  = LoginForm()
    if form.validate_on_submit():
        # Check if the email already exists
        user = User.query.filter_by(email= form.data.get('email')).first()
        if not user:
            flash('The email your provided does not exists.')
            return redirect(url_for('auth.login'))
        # Check password
        elif not check_password_hash(user.password, form.data.get('password')):
            flash('Ivalid password')
            return redirect(url_for('auth.login'))
        remember = True if form.data.get('remember_me') else False
        # Log the user In
        login_user(user, remember=remember)
        return redirect(url_for('main.home'))
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))