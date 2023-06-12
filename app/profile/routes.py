from . import profile
from flask_login import login_required, current_user
from app.models import User
from flask import render_template, current_app, flash, redirect, url_for
from sqlalchemy.orm import joinedload
from app.forms import FinishProfile
from app import csrf, db
import uuid, os
from werkzeug.utils import secure_filename
@profile.route('/profile')
@login_required
def profile_info():
    return render_template('profile/profile.html')


@profile.route('/edit_profile', methods=['POST', 'GET'])
@login_required
@csrf.exempt
def edit_profile():
    form = FinishProfile()
    if form.validate_on_submit():
        pro_pic = form.data.get('pro_pic')
        bio = form.data.get('bio')

        def save_profile_picture(pic):
            uuid1_value = uuid.uuid1()
            filename = str(uuid1_value) + secure_filename(pic.filename)
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.email, 'profile_pictures', filename)                
            pic.save(path)
            return os.path.join('profile_pictures', filename)
    

        try:
            if pro_pic:
                current_user.profile_pic=save_profile_picture(pro_pic)
            elif bio:
                current_user.user_bio=bio
            db.session.add(current_user)
            db.session.commit()
            flash('Your profile has been saved.')
            return redirect(url_for('profiles.profile_info'))
        except Exception as e:
            flash("Something Went wrong. Please try again!")
            return redirect(url_for('profiles.edit_profile'))

    return render_template('profile/edit_profile.html', form=form)

@profile.route('/user_profile/<int:user_id>')
@login_required
def user_profile(user_id):
    if user_id == current_user.id:
        return redirect(url_for('profiles.profile_info'))
    user = User.query.get_or_404(user_id)
    if user:
        return render_template('profile/user_profile.html', user=user)