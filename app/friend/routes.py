from . import friend
from flask_login import current_user, login_required
from app.models import FriendRequest, User
from app import db
from flask import redirect, url_for, flash, render_template
from sqlalchemy.exc import IntegrityError, OperationalError

@friend.route('/friend/request_list')
@login_required
def friends_request_list():
    query = db.session.query(User).join(FriendRequest, FriendRequest.friend_id == User.id).filter(FriendRequest.user_id == current_user.id)
    friends_list = query.all()
    return render_template('friend/request_friends.html', friends_list=friends_list)

@friend.route('/friend/add/<int:friend_id>')
@login_required
def add_friend(friend_id):
    user = User.query.get_or_404(friend_id)
    if user:
        friend = FriendRequest(user_id=friend_id, friend_id=current_user.id)
        try:
            db.session.add(friend)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash(f'You have already sent a friend request to {user.first_name} {user.last_name}!')
            return redirect(url_for('main.home'))
    flash('Friend request sent successfully!')
    return redirect(url_for('main.home'))

@friend.route('/friend/request_list/delete/<friend_id:int>')
@login_required
def delete_friend_request(friend_id):
    friend = FriendRequest.query.filter_by(friend_id=friend_id).first()
    if friend:
        try:
            db.session.delete(friend)
            db.session.commit()
        except Exception as e:
            flash(f'Something Went wrong while deleting {friend.firstname} from your friend requests!')
            return redirect(url_for('main.home'))
        finally:
            flash(f'{friend.first_name} {friend.last_name} has been removed succesfully from your friend requests.')
            return redirect(url_for('main.home'))