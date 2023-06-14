from . import friend
from flask_login import current_user, login_required
from app.models import FriendRequest, User, FriendList
from app import db
from flask import redirect, url_for, flash, render_template, abort, jsonify, request
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy import and_

@friend.route('/friends')
@login_required
def friends_list():
    # I'm smart asf
    friends_list = current_user.friends
    return render_template('friend/friends_list.html', friends_list=friends_list)


@friend.route('/friend/requests')
@login_required
def friend_requests():
    query = db.session.query(User).join(FriendRequest, FriendRequest.friend_id == User.id).filter(FriendRequest.user_id == current_user.id)
    # friends requests list
    friends_list = query.all()
    return render_template('friend/friend_requests.html', friends_list=friends_list)

@friend.route('/friend/add/<int:friend_id>')
@login_required
def send_friend_request(friend_id):
    user = User.query.get_or_404(friend_id)
    if user in current_user.friends:
        flash(f"{user.first_name} is Already a friend of you in Abook ofc hehe.")
        return redirect(url_for('main.home'))
    elif user:
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

@friend.route('/friend/requests/delete/<int:friend_id>')
@login_required
def delete_friend_request(friend_id):
    friend = FriendRequest.query.filter_by(friend_id=friend_id).first()
    user   = User.query.get_or_404(friend_id)
    if friend and user:
        username = f"{user.first_name} {user.last_name}"
        try:
            db.session.delete(friend)
            db.session.commit()
            flash(f'{username} has been removed successfully from your friend requests.')
        except IntegrityError:
            db.session.rollback()
            flash(f'Something went wrong while deleting {username} from your friend requests!')
        except OperationalError:
            db.session.rollback()
            flash('An unexpected error occurred. Please try again later.')
    else:
        abort(404, "Friend is not found!")

    return redirect(url_for('main.home'))

@friend.route('/friend/accept/<int:friend_id>')
@login_required
def accept_friend_request(friend_id):
    friend_req = FriendRequest.query.filter_by(friend_id=friend_id).first()
    friend = User.query.get_or_404(friend_id)
    username = f"{friend.first_name} {friend.last_name}"
    
    if friend_req and friend:
        friend_user  = FriendList.query.filter(and_(FriendList.friend_id == current_user.id, FriendList.user_id == friend_id)).first()
        if friend in current_user.friends or friend_user:
            flash(f"{username} is already in your friends list")
            db.session.delete(friend_req)
            db.session.commit()

        else:
            # to avoid all the confusing
            acc_fr = FriendList(user_id=current_user.id, friend_id=friend.id)
            acc2_fr= FriendList(user_id=friend.id, friend_id=current_user.id)
            try:
                db.session.add(acc_fr)
                db.session.add(acc2_fr)
                db.session.delete(friend_req)
                db.session.commit()
                flash(f"{username} is your friend now!")
            except Exception as e:
                db.session.rollback()
                flash(f"Error: {str(e)}")
    else:
        abort(404)

    return redirect(url_for('friend.friend_requests'))


# Delete a friend 
@friend.route('/friend/delete/<int:friend_id>')
@login_required
def delete_friend(friend_id):
    # check if the friend does exits as a user
    friend = User.query.get_or_404(friend_id)
    # check if the friend is in the current_user friends lists
    if friend and friend in current_user.friends:
        fr_col_1 = FriendList.query.filter(and_(FriendList.friend_id==friend_id, FriendList.user_id==current_user.id)).first()
        # Get the sec column of the friend ship
        fr_col_2 = FriendList.query.filter(and_(FriendList.friend_id==current_user.id, FriendList.user_id==friend_id)).first()
        # delete the friendship 
        try:
            db.session.delete(fr_col_1)
            db.session.delete(fr_col_2)
            db.session.commit()
            flash(f"You have unfraind {friend.first_name}.")
        except SQLAlchemyError as e:
             db.session.rollback()
             flash(f"Error occurred while deleting the friend: {str(e)}")
            
    return redirect(url_for('friend.friends_list'))