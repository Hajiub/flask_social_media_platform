from . import auth
from flask import session, request, url_for, render_template, redirect,  flash, current_app, abort
from app.forms import SigninForm, LoginForm
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
import os
from app import csrf, limiter
from .utils import MakeFolder

@auth.route('/signin', methods=['POST', 'GET'])
@csrf.exempt
@limiter.limit("10 per day")
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SigninForm()
    if form.validate_on_submit():
        user = User(
                username   = form.data.get('first_name') + ' ' + form.data.get('last_name'),
                email      = form.data.get('email'),
                password   = generate_password_hash(form.data.get('password1'), 'sha256'),
               
        )
        try:
            db.session.add(user)
            db.session.commit()
            user_dep = MakeFolder(current_app, user=user)
            user_dep.make_folder()
            # redirect to finish profile page with login the user 
            login_user(user)
            return redirect(url_for('profiles.finish_profile'))
        except Exception as e:
            flash('Something went wrong. Please try again! Error: ' + str(e))
            return redirect(url_for('auth.signin'))
    return render_template('auth/signin.html', form=form)

@auth.route('/login', methods=['POST', 'GET'])
@csrf.exempt
@limiter.limit("10 per hour", error_message="Please Try again Later!")
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

# @auth.errorhandler(429)
# def to_many_request(e):
#     return render_template('error/many_requests.html')