from . import profile
from flask_login import login_required, current_user
from app.models import User, Profile
from flask import render_template, current_app, flash, redirect, url_for
from sqlalchemy.orm import joinedload
from app.forms import EditProfileForm, FinishProfileForm
from app import csrf, db
import uuid, os
from werkzeug.utils import secure_filename
from .utils import SaveProfilePicture


@profile.route('/profile')
@login_required
def profile_info():
    return render_template('profile/profile.html')


@profile.route('/profile/edit', methods=['POST', 'GET'])
@login_required
@csrf.exempt
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        pro_pic = form.data.get('pro_pic')
        bio = form.data.get('bio')
        try:
            if pro_pic:
                save_pic_obj = SaveProfilePicture(current_app, current_user)
                current_user.profile_pic=save_pic_obj.save_profile_picture(pro_pic)
            if bio:
                current_user.user_bio=bio
            db.session.commit()
            flash('Your profile has been saved.')
            return redirect(url_for('profiles.profile_info'))
        except Exception as e:
            flash("Something Went wrong. Please try again! {0}".format(str(e)))
            return redirect(url_for('profiles.edit_profile'))

    return render_template('profile/edit_profile.html', form=form)

@profile.route('/profile/<int:user_id>')
@login_required
def user_profile(user_id):
    if user_id == current_user.id:
        return redirect(url_for('profiles.profile_info'))
    user = User.query.get_or_404(user_id)
    if user:
        return render_template('profile/user_profile.html', user=user)
    

@profile.route('/profile/finish', methods=['POST', 'GET'])
@login_required
@csrf.exempt # finish profile has a form
def finish_profile():
    return 