from . import auth
from flask import session, request, url_for, render_template, redirect, abort, flash, current_app
from app.forms import SigninForm, LoginForm
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
import os


@auth.route('/signin', methods=['POST', 'GET'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SigninForm()
    if form.validate_on_submit():
        if session.get('_csrf_token') != request.form.get('_csrf_token'):
            return abort(400, 'Invalid CSRF Token')
        try:
            user = User(
                first_name = form.data.get('first_name'),
                last_name  = form.data.get('last_name'),
                email      = form.data.get('email'),
                password   = generate_password_hash(form.data.get('password1'), 'sha256'),
                birthday   = form.data.get('birthday'),
            )
            db.session.add(user)
            db.session.commit()
            user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], user.email)
            post_images_folder = os.path.join(user_folder, "post_images")
            profile_pictures_folder = os.path.join(user_folder, "profile_pictures")
            os.makedirs(user_folder, exist_ok=True)
            os.makedirs(post_images_folder, exist_ok=True)
            os.makedirs(profile_pictures_folder, exist_ok=True)
        except Exception as e:
            flash('Something went wrong. Please try again! Error: ' + str(e))
            return redirect(url_for('auth.signin'))
        return redirect(url_for('auth.login'))
    return render_template('auth/signin.html', form=form)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form  = LoginForm()
    if form.validate_on_submit():
        if session.get('_csrf_token') != request.form.get('_csrf_token'):
            return abort(400, 'Invalid CSRF Token')
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